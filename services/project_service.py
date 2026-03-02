import json
from pathlib import Path
from models.project import Project

PROJECTS_FILE = Path("data/projects.json")

# Functions to load, save, and create projects. These functions handle reading from and writing to the projects.json file, as well as creating new Project objects with unique IDs and saving them to the file.
def load_projects():
    if not PROJECTS_FILE.exists():
        return []

    with open(PROJECTS_FILE, "r") as f:
        try:
            projects_data = json.load(f)
        except json.JSONDecodeError:
            projects_data = []

    return [Project(**p) for p in projects_data] # For every dictionary inside projects_data, creates a Project object by unpacking the dictionary as keyword arguments. 
    #This assumes that the keys in the dictionary match the parameters of the Project class constructor


def save_projects(projects):
    with open(PROJECTS_FILE, "w") as f:
        json.dump([p.__dict__ for p in projects], f, indent=4) 
        """Converts each Project object to a 
        dictionary using __dict__ and saves as JSON with indentation for readability"""


def create_project(name, description, owner_id): # Creates a new project with a unique ID, the provided name, description, and owner_id, and an empty list of member_ids. 
    #new project is then saved to the JSON file and returns the created Project object.
    projects = load_projects()

    if projects:
        new_id = max(p.id for p in projects) + 1 #Find the maximum existing project ID and add 1 to create a new unique ID for the new project
    else:
        new_id = 1

    new_project = Project(
        id=new_id,
        name=name,
        description=description,
        owner_id=owner_id,
        member_ids=[] # New projects start with an empty list of member IDs.
         # Members can be added later using a separate function. Project starts with only owner as a member, but owner_id is stored separately to easily identify the project owner.
    )

    projects.append(new_project)
    save_projects(projects)

    return new_project

# This function checks if a given user (identified by user_id) has access to a project. A user has access if they are either the owner 
# of the project or if their user ID is in the list of member IDs for the project. The function returns True if the user has access and False otherwise.
def user_has_project_access(project, user_id):
    if project.owner_id == user_id:
        return True

    if user_id in project.member_ids:
        return True

    return False