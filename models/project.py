from datetime import datetime

class Project:
    def __init__(
        self,
        id,
        name,
        description,
        owner_id,
        member_ids,
        created_at=None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.member_ids = member_ids

        if created_at:
            self.created_at = created_at
        else:
            self.created_at = datetime.now().isoformat()