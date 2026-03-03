from datetime import datetime, timezone


class Project:
    """Represents a project with owner and team members.

    Attributes are encapsulated with property getters/setters for validation.
    """

    def __init__(
        self,
        id,
        name,
        description,
        owner_id,
        member_ids=None,
        created_at=None,
    ):
        self._id = id
        self._name = name
        self._description = description
        self._owner_id = owner_id
        self._member_ids = member_ids if member_ids is not None else []
        self._created_at = created_at or datetime.now(timezone.utc).isoformat()

    @property
    def id(self):
        """Unique project identifier (read-only)."""
        return self._id

    @property
    def name(self):
        """Project name."""
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Project name must be a non-empty string")
        self._name = value

    @property
    def description(self):
        """Project description."""
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError("Description must be a string")
        self._description = value

    @property
    def owner_id(self):
        """User ID of the project owner (read-only)."""
        return self._owner_id

    @property
    def member_ids(self):
        """List of user IDs assigned to this project."""
        return self._member_ids

    @member_ids.setter
    def member_ids(self, value):
        if not isinstance(value, list):
            raise ValueError("member_ids must be a list")
        self._member_ids = value

    @property
    def created_at(self):
        """ISO format timestamp of project creation (read-only)."""
        return self._created_at

    def __repr__(self):
        return f"Project(id={self._id}, name='{self._name}', owner_id={self._owner_id})"

    def __str__(self):
        return f"Project: {self._name} (ID: {self._id})"