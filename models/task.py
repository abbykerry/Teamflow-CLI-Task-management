# models/task.py

from datetime import datetime, timezone


class Task:
    """Represents a task within a project with proper encapsulation.

    All attributes are accessed via properties; validation is enforced
    in setters. The constructor supports an optional creation timestamp.
    """

    def __init__(
        self,
        id: int,
        project_id: int,
        title: str,
        assigned_to: int | None,
        status: str,
        created_at: str = None,
    ):
    #these attributes are protected because we want to enforce validation through the property setters. 
    # For example, we want to ensure that the title is always a non-empty string and that assigned_to 
    # is either an integer user ID or None. By using properties, 
    # we can add this validation logic in one place and ensure that any code that tries to set these 
    # attributes will go through the proper checks.
        self._id = id
        self._project_id = project_id
        self._title = title
        self._assigned_to = assigned_to
        self._status = status
        self._created_at = created_at or datetime.now(timezone.utc).isoformat()

    @property
    def id(self) -> int:
        """Read-only task identifier."""
        return self._id

    @property
    def project_id(self) -> int:
        return self._project_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Task title must be a non-empty string")
        self._title = value

    @property
    def assigned_to(self) -> int | None:
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, user_id: int | None) -> None:
        if user_id is not None and not isinstance(user_id, int):
            raise ValueError("assigned_to must be an integer user ID or None")
        self._assigned_to = user_id

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, s: str) -> None:
        if not isinstance(s, str) or not s.strip():
            raise ValueError("Status must be a non-empty string")
        self._status = s

    @property
    def created_at(self) -> str:
        return self._created_at

    def __repr__(self):
        return f"Task(id={self._id}, title='{self._title}', status='{self._status}')"

    def __str__(self):
        return f"Task: {self._title} [{self._status}] (ID: {self._id})"