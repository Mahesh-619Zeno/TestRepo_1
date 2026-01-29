import json
import os
from tasks.task import Task

def export_tasks(task_manager, filename):
    """Export all tasks to a JSON file."""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        # Prepare task data (same format as save_tasks)
        data = [task.__dict__ for task in task_manager.tasks]
        
        # Write with UTF-8 encoding
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        count = len(task_manager.tasks)
        return f"Successfully exported {count} task(s) to '{filename}'."
    
    except PermissionError:
        return f"Error: Permission denied for '{filename}'."
    except OSError as e:
        return f"Error: Cannot write to '{filename}': {str(e)}"
    except Exception as e:
        return f"Error: Failed to export tasks: {str(e)}"

def import_tasks(task_manager, filename, overwrite=False):
    """Import tasks from JSON file with merge or overwrite behavior."""
    if not os.path.exists(filename):
        return f"Error: File '{filename}' not found."
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            return "Error: Import file must contain a JSON array."
        
        imported_count = 0
        updated_count = 0
        
        if overwrite:
            # Clear all existing tasks
            task_manager.tasks.clear()
            print("Cleared existing tasks (overwrite mode).")
        
        # Track existing titles for merge detection
        existing_titles = {t.title.lower(): t for t in task_manager.tasks}
        
        for task_data in data:
            try:
                # Validate required fields
                if not all(key in task_data for key in ['title']):
                    continue  # Skip invalid tasks
                
                title = task_data['title']
                
                # Create or update task
                if overwrite or title.lower() not in existing_titles:
                    # Add new task
                    task = Task(
                        title=task_data.get('title', ''),
                        description=task_data.get('description', ''),
                        priority=task_data.get('priority', 'Medium'),
                        status=task_data.get('status', 'Pending')
                    )
                    task_manager.tasks.append(task)
                    imported_count += 1
                else:
                    # Update existing task (merge mode)
                    existing_task = existing_titles[title.lower()]
                    for key, value in task_data.items():
                        if hasattr(existing_task, key):
                            setattr(existing_task, key, value)
                    updated_count += 1
            
            except Exception:
                # Skip individual invalid tasks
                continue
        
        # Save changes
        task_manager.save_tasks()
        
        status_msg = []
        if imported_count > 0:
            status_msg.append(f"Imported {imported_count} new task(s)")
        if updated_count > 0:
            status_msg.append(f"Updated {updated_count} existing task(s)")
        
        return f"Import complete: {'; '.join(status_msg)} from '{filename}'."
    
    except json.JSONDecodeError:
        return f"Error: '{filename}' is not valid JSON."
    except UnicodeDecodeError:
        return f"Error: Cannot read '{filename}' with UTF-8 encoding."
    except Exception as e:
        return f"Error: Failed to import from '{filename}': {str(e)}"
