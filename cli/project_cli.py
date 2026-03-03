# cli/project_cli.py

from services.project_service import (
    create_project,
    load_projects,
    assign_user_to_project,
    user_has_project_access,
)
from services.user_service import load_users
from cli import menu

# optional rich support for pretty tables
try:
    from rich.console import Console
    from rich.table import Table
    console = Console()
    USE_RICH = True
except ImportError:  # rich not installed
    console = None
    USE_RICH = False


def create_project_action(session):
    """Prompt and create a new project (admin-only via menu guard)."""
    user = session.current_user
    name = input("Enter project name: ").strip()
    description = input("Enter project description: ").strip()

    new_project = create_project(
        name=name,
        description=description,
        owner_id=user.id,
    )

    print(f"\n✅ Project '{new_project.name}' created successfully (ID: {new_project.id})")


def assign_user_action(session):
    """Display projects and users, then assign a member (admin-only via menu guard)."""
    # Show projects
    projects = load_projects()
    if not projects:
        print("\n⚠️ No projects exist yet.")
        return

    if USE_RICH:
        console.print("\n[bold underline]AVAILABLE PROJECTS[/bold underline]")
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID", justify="right")
        table.add_column("Name")
        for p in projects:
            table.add_row(str(p.id), p.name)
        console.print(table)
    else:
        print("\n=== AVAILABLE PROJECTS ===")
        for p in projects:
            print(f"ID: {p.id} | Name: {p.name}")

    # Show users
    users = load_users()
    if USE_RICH:
        console.print("\n[bold underline]AVAILABLE USERS[/bold underline]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", justify="right")
        table.add_column("Username")
        table.add_column("Role")
        for u in users:
            table.add_row(str(u.id), u.username, u.role)
        console.print(table)
    else:
        print("\n=== AVAILABLE USERS ===")
        for u in users:
            print(f"ID: {u.id} | Username: {u.username} | Role: {u.role}")

    try:
        project_id = int(input("\nEnter project ID: ").strip())
        user_id = int(input("\nEnter user ID to assign: ").strip())

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
                if USE_RICH:
                    console.print("\n[bold underline]YOUR PROJECTS[/bold underline]")
                    table = Table(show_header=True, header_style="bold green")
                    table.add_column("ID", justify="right")
                    table.add_column("Name")
                    table.add_column("Description")
                    for project in user_projects:
                        table.add_row(str(project.id), project.name, project.description)
                    console.print(table)
                else:
                    print("\n=== YOUR PROJECTS ===")
                    for project in user_projects:
                        print(f"ID: {project.id} | Name: {project.name} | Description: {project.description}")
        elif choice == "4":
            break
        else:
            print("\n⚠️ Invalid project option selected.")