from datetime import datetime

class Project:
    def __init__(
        self,
        id,
        name,
        description,
        owner_id,
        member_ids,
        created_at=None # Optional, will be set to current time if not provided
    ):
        self.id = id
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.member_ids = member_ids

        if created_at:
            self.created_at = created_at # Use provided created_at if given (e.g., when loading from JSON)
        else:
            self.created_at = datetime.now().isoformat() # Set to current time in ISO format if not provided (e.g., when creating a new project)

    def __repr__(self):
        return f"Project(id={self.id}, name='{self.name}', owner_id={self.owner_id})"

    def __str__(self):
        return f"Project: {self.name} (ID: {self.id})"