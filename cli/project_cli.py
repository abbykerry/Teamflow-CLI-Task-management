# cli/project_cli.py

from services.project_service import create_project, load_projects, assign_user_to_project, user_has_project_access
from services.user_service import load_users
from utils.decorators import require_role
from cli import menu


@require_role('admin')
def create_project_action(session):
    """Admin-only: Prompt and create a new project"""
    user = session.current_user
    name = input("Enter project name: ").strip()
    description = input("Enter project description: ").strip()

    new_project = create_project(
        name=name,
        description=description,
        owner_id=user.id
    )

    print(f"\n✅ Project '{new_project.name}' created successfully (ID: {new_project.id})")


@require_role('admin')
def assign_user_action(session):
    """Admin-only: Display projects and users, then assign a member"""
    # Show projects
    projects = load_projects()
    if not projects:
        print("\n⚠️ No projects exist yet.")
        return
    
    print("\n=== AVAILABLE PROJECTS ===")
    for p in projects:
        print(f"ID: {p.id} | Name: {p.name}")

    # Show users
    users = load_users()
    print("\n=== AVAILABLE USERS ===")
    for u in users:
        print(f"ID: {u.id} | Username: {u.username} | Role: {u.role}")

    try:
        project_id = int(input("\nEnter project ID: ").strip())
        user_id = int(input("Enter user ID to assign: ").strip())
        
        if assign_user_to_project(project_id, user_id):
            print(f"\n✅ User {user_id} assigned to project {project_id} successfully.")
        else:
            print(f"\n❌ Project {project_id} not found.")
    except ValueError:
        print("\n❌ Error: IDs must be integers.")


def handle_project_actions(session):
    """
    Handles project-related actions. Re-displays the projects menu until the
    user chooses to go back.
    """
    user = session.current_user
    while True:
        choice = menu.projects_menu()

        if choice == "1":
            create_project_action(session)
        elif choice == "2":
            assign_user_action(session)
        elif choice == "3":
            projects = load_projects()
            user_projects = [p for p in projects if user_has_project_access(p, user.id)]

            if not user_projects:
                print("\n📭 You have no projects yet.")
            else:
                print("\n=== YOUR PROJECTS ===")
                for project in user_projects:
                    print(f"ID: {project.id} | Name: {project.name} | Description: {project.description}")
        elif choice == "4":
            break
        else:
            print("\n⚠️ Invalid project option selected.")