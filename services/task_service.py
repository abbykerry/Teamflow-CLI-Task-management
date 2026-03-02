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

        return [Task(**t) for t in tasks_data]
    except Exception as e:
        logger.exception(f"Error loading tasks: {e}")
        return []

def save_tasks(tasks):
    try:
        with open(TASKS_FILE, "w") as f:
            json.dump([t.__dict__ for t in tasks], f, indent=4)
        logger.info(f"Saved {len(tasks)} tasks")
    except Exception as e:
        logger.error(f"Error saving tasks: {e}")
        raise

def create_task(project_id, title, assigned_to=None, status="todo"):
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