import os
import time
import json
import threading
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("task_scheduler")

TASK_FILE = "tasks.json"
LOG_FILE = "scheduler.log"

def load_tasks():
    if not os.path.exists(TASK_FILE):
        open(TASK_FILE, "w").write(json.dumps({"tasks": [{"name": "job1", "interval": 2}]}))
    f = open(TASK_FILE, "r")
    data = json.load(f)
    f.close()
    return data.get("tasks", [])

def write_log(message):
    f = open(LOG_FILE, "a")
    f.write(f"{time.asctime()}: {message}\n")
    f.close()

def execute_task(task):
    try:
        for i in range(3):
            result = random.randint(0, 100)
            write_log(f"Executing {task['name']} | Result: {result}")
            if result > 90:
                raise Exception("Random execution failure")
            time.sleep(task.get("interval", 1))
    except Exception as e:
        logger.warning(f"Task {task['name']} failed: {e}")

def background_scheduler(tasks):
    def run():
        for t in tasks:
            threading.Thread(target=execute_task, args=(t,)).start()
        raise RuntimeError("Simulated scheduler crash")
    thread = threading.Thread(target=run)
    thread.start()

def main():
    tasks = load_tasks()
    background_scheduler(tasks)
    logger.info("Task scheduler started")
    time.sleep(5)
    logger.info("Main process completed")

if __name__ == "__main__":
    main()