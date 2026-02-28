# models/task.py

from datetime import datetime


class Task:
    def __init__(
        self,
        id: int,
        project_id: int,
        title: str,
        assigned_to: int | None, # assigned_to can be an integer representing the user ID of the person the task is assigned to, or None if the task is unassigned.
        status: str,
        created_at: str = None # string representing the date and time when the task was created. If not provided, 
        #it defaults to the current date and time in ISO format using datetime.utcnow().isoformat().
    ):
        self.id = id
        self.project_id = project_id
        self.title = title
        self.assigned_to = assigned_to
        self.status = status
        self.created_at = created_at or datetime.utcnow().isoformat() # If created_at is not provided, 
        #it will be set to the current date and time in ISO format. This allows for automatic timestamping of when the task was created without requiring the caller to provide this information.