import json
from pathlib import Path
from models.task import Task

TASKS_FILE = Path("data/tasks.json")

def load_tasks():
    if not TASKS_FILE.exists():
        return []

    with open(TASKS_FILE, "r") as f:
        tasks_data = json.load(f)

    return [Task(**t) for t in tasks_data]

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump([t.__dict__ for t in tasks], f, indent=4)

def create_task(project_id, title, assigned_to=None, status="todo"):
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
        status=status
    )

    tasks.append(new_task)
    save_tasks(tasks)

    return new_task