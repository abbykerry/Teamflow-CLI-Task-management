import os
import json
from pathlib import Path
from models.task import Task
from utils.logger import get_logger

logger = get_logger('task_service')

DATA_DIR = Path(os.getenv('DATA_DIR', 'data'))
TASKS_FILE = DATA_DIR / "tasks.json"

def load_tasks():
    try:
        if not TASKS_FILE.exists():
            logger.debug(f"Tasks file not found at {TASKS_FILE}")
            return []

        with open(TASKS_FILE, "r") as f:
            try:
                tasks_data = json.load(f)
                logger.info(f"Loaded {len(tasks_data)} tasks")
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                tasks_data = []

        # Normalize keys from private attributes to public parameter names
        normalized = []
        for t in tasks_data:
            normalized_t = {
                'id': t.get('_id', t.get('id')),
                'project_id': t.get('_project_id', t.get('project_id')),
                'title': t.get('_title', t.get('title')),
                'assigned_to': t.get('_assigned_to', t.get('assigned_to')),
                'status': t.get('_status', t.get('status')),
                'created_at': t.get('_created_at', t.get('created_at')),
            }
            normalized.append(normalized_t)
        return [Task(**t) for t in normalized]
    except Exception as e:
        logger.exception(f"Error loading tasks: {e}")
        return []

def save_tasks(tasks):
    try:
        # Normalize private attributes to public names for JSON
        data = []
        for t in tasks:
            t_dict = t.__dict__.copy()
            # Map private to public names
            t_dict['id'] = t_dict.pop('_id', None)
            t_dict['project_id'] = t_dict.pop('_project_id', None)
            t_dict['title'] = t_dict.pop('_title', None)
            t_dict['assigned_to'] = t_dict.pop('_assigned_to', None)
            t_dict['status'] = t_dict.pop('_status', None)
            t_dict['created_at'] = t_dict.pop('_created_at', None)
            data.append(t_dict)
        
        with open(TASKS_FILE, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Saved {len(tasks)} tasks")
    except Exception as e:
        logger.error(f"Error saving tasks: {e}")
        raise

def create_task(project_id, title, description="", assigned_to=None, status="todo"):
    try:
        tasks = load_tasks()

        if tasks:
            new_id = max(t.id for t in tasks) + 1
        else:
            new_id = 1

        new_task = Task(
            id=new_id,
            project_id=project_id,
            title=title,
            assigned_to=assigned_to,
            status=status,
        )

        tasks.append(new_task)
        save_tasks(tasks)
        logger.info(f"Created task {title} (ID {new_id})")
        return new_task
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise

def get_tasks_by_project(project_id):
    tasks = load_tasks()

    project_tasks = [
        task for task in tasks
        if task.project_id == project_id
    ]

    return project_tasks

def update_task(task_id, title=None, assigned_to=None, status=None):
    """Updates a task's title, assignee, or status."""
    try:
        tasks = load_tasks()
        for t in tasks:
            if t.id == task_id:
                has_changes = False
                if title and t.title != title:
                    t.title = title
                    has_changes = True
                if assigned_to is not None and t.assigned_to != assigned_to:
                    t.assigned_to = assigned_to
                    has_changes = True
                if status and t.status != status:
                    t.status = status
                    has_changes = True
                
                if has_changes:
                    save_tasks(tasks)
                    logger.info(f"Updated task {task_id}")
                return True
        return False
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {e}")
        return False

def unassign_task(task_id):
    """Removes assignee from a task (sets assigned_to to None)."""
    try:
        tasks = load_tasks()
        for t in tasks:
            if t.id == task_id:
                t.assigned_to = None
                save_tasks(tasks)
                logger.info(f"Unassigned task {task_id}")
                return True
        return False
    except Exception as e:
        logger.error(f"Error unassigning task {task_id}: {e}")
        return False

def delete_task(task_id):
    """Deletes a task by ID."""
    try:
        tasks = load_tasks()
        initial_count = len(tasks)
        tasks = [t for t in tasks if t.id != task_id]
        if len(tasks) < initial_count:
            save_tasks(tasks)
            logger.info(f"Deleted task {task_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {e}")
        return False