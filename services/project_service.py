import os
import json
from pathlib import Path
from models.project import Project
from utils.logger import get_logger

logger = get_logger('project_service')

# base data directory controlled by environment variable
DATA_DIR = Path(os.getenv('DATA_DIR', 'data'))
PROJECTS_FILE = DATA_DIR / "projects.json"

# Functions to load, save, and create projects. These functions handle reading from and writing to the projects.json file, as well as creating new Project objects with unique IDs and saving them to the file.
def load_projects():
    try:
        if not PROJECTS_FILE.exists():
            logger.debug(f"Projects file not found at {PROJECTS_FILE}")
            return []

        with open(PROJECTS_FILE, "r") as f:
            try:
                projects_data = json.load(f)
                logger.info(f"Loaded {len(projects_data)} projects")
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                projects_data = []

        # Normalize keys from private attributes to public parameter names
        normalized = []
        for p in projects_data:
            normalized_p = {
                'id': p.get('_id', p.get('id')),
                'name': p.get('_name', p.get('name')),
                'description': p.get('_description', p.get('description')),
                'owner_id': p.get('_owner_id', p.get('owner_id')),
                'member_ids': p.get('_member_ids', p.get('member_ids')),
                'created_at': p.get('_created_at', p.get('created_at')),
            }
            normalized.append(normalized_p)
        return [Project(**p) for p in normalized]
    except Exception as e:
        logger.exception(f"Error loading projects: {e}")
        return []


def save_projects(projects):
    try:
        # Normalize private attributes to public names for JSON
        data = []
        for p in projects:
            p_dict = p.__dict__.copy()
            # Map private to public names
            p_dict['id'] = p_dict.pop('_id', None)
            p_dict['name'] = p_dict.pop('_name', None)
            p_dict['description'] = p_dict.pop('_description', None)
            p_dict['owner_id'] = p_dict.pop('_owner_id', None)
            p_dict['member_ids'] = p_dict.pop('_member_ids', None)
            p_dict['created_at'] = p_dict.pop('_created_at', None)
            data.append(p_dict)
        
        with open(PROJECTS_FILE, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Saved {len(projects)} projects")
    except Exception as e:
        logger.error(f"Error saving projects: {e}")
        raise


def create_project(name, description, owner_id):
    try:
        projects = load_projects()

        if projects:
            new_id = max(p.id for p in projects) + 1
        else:
            new_id = 1

        new_project = Project(
            id=new_id,
            name=name,
            description=description,
            owner_id=owner_id,
            member_ids=[],
        )

        projects.append(new_project)
        save_projects(projects)
        logger.info(f"Created project {name} (ID {new_id})")
        return new_project
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise

# This function checks if a given user (identified by user_id) has access to a project. A user has access if they are either the owner 
# of the project or if their user ID is in the list of member IDs for the project. The function returns True if the user has access and False otherwise.
def user_has_project_access(project, user_id):
    if project.owner_id == user_id:
        return True

    if project.member_ids is None:
        project.member_ids = []

    if user_id in project.member_ids:
        return True

    return False


def assign_user_to_project(project_id, user_id):
    """Assigns a user to a project by adding their user ID to the project's member list."""
    try:
        projects = load_projects()
        for p in projects:
            if p.id == project_id:
                if p.member_ids is None:
                    p.member_ids = []
                if user_id not in p.member_ids:
                    p.member_ids.append(user_id)
                    save_projects(projects)
                    logger.info(f"Assigned user {user_id} to project {project_id}")
                else:
                    logger.debug(f"User {user_id} already member of project {project_id}")
                return True
        logger.warning(f"Project {project_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error assigning user: {e}")
        raise