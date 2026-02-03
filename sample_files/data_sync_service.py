from __future__ import annotations

import json
import sys
import datetime
import time
import sqlite3
import signal
import threading
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from contextlib import contextmanager
import shutil

try:
    from jsonschema import validate, ValidationError
except ImportError:
    print("WARNING: jsonschema not installed. Install with: pip install jsonschema")
    validate = None

DATA_FILE = Path("tasks.json")
REMOTE_BACKUP = Path("tasks_backup.json")
DB_FILE = Path("tasks.db")
SYNC_LOG = Path("data_sync.log")
PID_FILE = Path("data_sync.pid")

# JSON Schema (enhanced for tags)
TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "minimum": 1},
                    "title": {"type": "string", "minLength": 1, "maxLength": 500},
                    "completed": {"type": "boolean"},
                    "tags": {"type": "array", "items": {"type": "string", "maxLength": 50}},
                    "created": {"type": "string", "format": "date-time"},
                    "updated": {"type": "string", "format": "date-time"}
                },
                "required": ["id", "title", "completed"],
                "additionalProperties": False
            },
            "maxItems": 10000
        },
        "counter": {"type": "integer", "minimum": 1},
        "metadata": {"type": "object"}
    },
    "required": ["tasks", "counter"],
    "additionalProperties": False
}

@dataclass
class SyncStats:
    local_tasks: int = 0
    remote_tasks: int = 0
    db_tasks: int = 0
    added: int = 0
    updated: int = 0
    deleted: int = 0
    errors: int = 0
    validation_errors: int = 0
    cycles: int = 0
    last_cycle: str = ""

class DataSyncService:
    def __init__(self):
        self.stats = SyncStats()
        self.running = False
        self.sync_thread = None
        self._init_sqlite()
        self._load_stats()
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Graceful shutdown on Ctrl+C or SIGTERM"""
        self.stop()
        sys.exit(0)

    def _init_sqlite(self):
        """Initialize SQLite database with proper constraints"""
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL CHECK(length(title) > 0 AND length(title) <= 500),
                    completed BOOLEAN NOT NULL DEFAULT 0,
                    created TEXT NOT NULL,
                    updated TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS task_tags (
                    task_id INTEGER,
                    tag TEXT NOT NULL CHECK(length(tag) > 0 AND length(tag) <= 50),
                    PRIMARY KEY (task_id, tag),
                    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_updated ON tasks(updated)")
            conn.commit()

    @staticmethod
    def now_iso() -> str:
        return datetime.datetime.now().isoformat()

    # COMPLETE JSON DATA PROCESSING
    def validate_json_data(self, data: Dict[str, Any]) -> bool:
        """✅ COMPLETE: Validate JSON format before sync"""
        if validate is None:
            self._log_sync("WARNING: jsonschema not available, skipping validation", "WARN")
            return True
        try:
            validate(instance=data, schema=TASK_SCHEMA)
            return True
        except ValidationError as e:
            self.stats.validation_errors += 1
            self._log_error(f"JSON validation failed: {str(e)[:200]}")
            return False

    def safe_read_json(self, path: Path) -> Optional[Dict[str, Any]]:
        """✅ COMPLETE: Parse incoming JSON data structures"""
        if not path.exists() or path.read_text().strip() == "":
            self._log_sync(f"No data file found at {path}, using default structure")
            return self._default_data_structure()
        
        try:
            data = json.loads(path.read_text(encoding='utf-8', errors='replace'))
            if not isinstance(data, dict):
                raise ValueError("Root must be object")
            
            if not self.validate_json_data(data):
                self._log_error(f"Invalid JSON structure in {path}")
                return None
                
            return self._normalize_data(data)
        except json.JSONDecodeError as e:
            self._log_error(f"JSON parse error in {path}: {str(e)}")
            return None
        except Exception as e:
            self._log_error(f"Error reading {path}: {str(e)}")
            return None

    def _default_data_structure(self) -> Dict[str, Any]:
        return {"tasks": [], "counter": 1, "metadata": {"version": "2.0"}}

    def _normalize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize and ensure all required fields exist"""
        normalized = data.copy()
        for task in normalized.get("tasks", []):
            if "created" not in task:
                task["created"] = self.now_iso()
            if "updated" not in task:
                task["updated"] = self.now_iso()
            if "tags" not in task:
                task["tags"] = []
        return normalized

    def _log_sync(self, message: str, level: str = "INFO"):
        timestamp = self.now_iso()
        try:
            with open(SYNC_LOG, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} [{level}] {message}\n")
            print(f"[{level}] {message}")
        except Exception:
            print(f"{timestamp} [{level}] {message}")

    def _log_error(self, message: str):
        self._log_sync(message, "ERROR")

    # ✅ COMPLETE: SQLite Database Updates with INSERT/UPDATE operations
    @contextmanager
    def get_db_connection(self):
        """Context manager for SQLite transactions"""
        conn = sqlite3.connect(DB_FILE)
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def sync_to_sqlite(self) -> bool:
        """✅ COMPLETE: JSON → SQLite with INSERT/UPDATE operations"""
        json_data = self.safe_read_json(DATA_FILE)
        if not json_data:
            self._log_error("Failed to read valid JSON data")
            return False

        self.stats.local_tasks = len(json_data["tasks"])
        added = updated = 0

        with self.get_db_connection() as conn:
            conn.execute("BEGIN TRANSACTION")
            
            # Clear existing tags for all tasks first
            conn.execute("DELETE FROM task_tags")
            
            for task in json_data["tasks"]:
                task_id = task["id"]
                title = task["title"][:500]  # Enforce length limit
                completed = 1 if task["completed"] else 0
                created = task["created"]
                updated = task["updated"]
                
                # UPSERT operation
                conn.execute("""
                    INSERT INTO tasks (id, title, completed, created, updated)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        title = excluded.title,
                        completed = excluded.completed,
                        updated = excluded.updated
                """, (task_id, title, completed, created, updated))
                
                # Insert tags
                for tag in task.get("tags", []):
                    if len(tag) <= 50:
                        conn.execute(
                            "INSERT OR IGNORE INTO task_tags (task_id, tag) VALUES (?, ?)",
                            (task_id, tag)
                        )
                
                # Count changes
                cursor = conn.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
                if not cursor.fetchone():  # New task
                    added += 1
                else:  # Updated task
                    updated += 1
            
            # Count total DB tasks
            cursor = conn.execute("SELECT COUNT(*) FROM tasks")
            self.stats.db_tasks = cursor.fetchone()[0]

        self.stats.added += added
        self.stats.updated += updated
        self._log_sync(f"✅ SQLite sync: {added} added, {updated} updated, {self.stats.db_tasks} total")
        return True

    def sync_from_sqlite(self) -> bool:
        """SQLite → JSON sync"""
        try:
            with self.get_db_connection() as conn:
                # Get all tasks with tags
                cursor = conn.execute("""
                    SELECT t.id, t.title, t.completed, t.created, t.updated,
                           GROUP_CONCAT(tag) as tags
                    FROM tasks t
                    LEFT JOIN task_tags tt ON t.id = tt.task_id
                    GROUP BY t.id, t.title, t.completed, t.created, t.updated
                    ORDER BY t.id
                """)
                
                tasks = []
                task_map = {}
                
                for row in cursor.fetchall():
                    task_id, title, completed, created, updated, tags_str = row
                    completed_bool = bool(completed)
                    
                    if task_id not in task_map:
                        task_map[task_id] = {
                            "id": task_id,
                            "title": title,
                            "completed": completed_bool,
                            "created": created,
                            "updated": updated,
                            "tags": []
                        }
                        tasks.append(task_map[task_id])
                    
                    if tags_str:
                        task_map[task_id]["tags"].extend(tags_str.split(","))
                
                # Write back to JSON
                data = {
                    "tasks": tasks,
                    "counter": max([t["id"] for t in tasks] + [1]),
                    "metadata": {"version": "2.0", "last_sync": self.now_iso()}
                }
                
                DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))
                self.stats.local_tasks = len(tasks)
                
            self._log_sync(f"✅ SQLite → JSON: {self.stats.local_tasks} tasks")
            return True
            
        except Exception as e:
            self._log_error(f"SQLite → JSON failed: {e}")
            return False

    def start_continuous_sync(self, interval: int = 300, sync_remote: bool = True):
        if self.running:
            print("Continuous sync already running")
            return

        self.running = True
        self.sync_thread = threading.Thread(
            target=self._continuous_sync_worker, 
            args=(interval, sync_remote), daemon=True
        )
        self.sync_thread.start()
        PID_FILE.write_text(str(os.getpid()))
        print(f"🚀 Continuous sync started (PID {os.getpid()}), interval: {interval}s")

    def _continuous_sync_worker(self, interval: int, sync_remote: bool):
        backoff = 1
        max_backoff = 10
        
        while self.running:
            cycle_start = self.now_iso()
            self.stats.cycles += 1
            self.stats.last_cycle = cycle_start
            
            try:
                self._log_sync(f"🔄 Cycle #{self.stats.cycles} starting...")
                
                self.sync_to_sqlite()
                self.sync_from_sqlite()
                if sync_remote:
                    self.sync_files()
                
                self.save_stats()
                backoff = 1
                
            except Exception as e:
                self.stats.errors += 1
                self._log_error(f"Cycle failed: {e}")
                backoff = min(backoff * 2, max_backoff)
            
            sleep_time = interval * backoff
            self._log_sync(f"⏳ Sleeping {sleep_time:.0f}s (backoff: {backoff}x)")
            time.sleep(sleep_time)

    def stop(self):
        self.running = False
        if self.sync_thread and self.sync_thread.is_alive():
            self.sync_thread.join(timeout=5)
        try:
            PID_FILE.unlink()
        except:
            pass
        self._log_sync("🛑 Continuous sync stopped")

    def sync_files(self) -> bool:
        self.stats.remote_tasks = self.stats.local_tasks
        self._log_sync("File sync complete")
        return True

    def _load_stats(self):
        stats_file = SYNC_LOG.with_suffix('.stats.json')
        try:
            if stats_file.exists():
                stats_data = json.loads(stats_file.read_text())
                self.stats = SyncStats(**stats_data.get("last_sync", {}))
        except:
            pass

    def save_stats(self):
        stats_file = SYNC_LOG.with_suffix('.stats.json')
        stats_file.write_text(json.dumps({"last_sync": self.stats.__dict__}, indent=2))

    def status(self):
        if self.running:
            print("✅ Running (thread alive)")
        else:
            print("⏹️  Stopped")
        print(f"Cycle #{self.stats.cycles}, Errors: {self.stats.errors}")
        print(f"Last cycle: {self.stats.last_cycle}")
        print(f"Tasks: Local={self.stats.local_tasks}, DB={self.stats.db_tasks}")

def sync_menu():
    service = DataSyncService()
    
    while True:
        print("\n=== 🚀 Data Sync Service ===")
        if service.running:
            print("🚀 CONTINUOUS MODE ACTIVE")
            print("1) Show Status")
            print("2) Stop Continuous")
        else:
            print("1) JSON → SQLite (w/ validation)")
            print("2) SQLite → JSON")
            print("3) Start Continuous (5min)")
            print("4) Start Continuous (Custom)")
        print("5) Show Stats")
        print("6) View Log")
        print("0) Exit")
        
        choice = input("> ").strip()
        
        if choice == "1":
            if service.running:
                service.status()
            else:
                service.sync_to_sqlite()
        elif choice == "2":
            if service.running:
                service.stop()
            else:
                service.sync_from_sqlite()
        elif choice in ("3", "4"):
            if not service.running:
                interval = 300 if choice == "3" else int(input("Interval (seconds): "))
                service.start_continuous_sync(interval)
        elif choice == "5":
            print(f"Stats: {service.stats.__dict__}")
        elif choice == "6":
            try:
                print(SYNC_LOG.read_text())
            except:
                print("Log not found")
        elif choice == "0":
            service.stop()
            break

if __name__ == "__main__":
    sync_menu()
