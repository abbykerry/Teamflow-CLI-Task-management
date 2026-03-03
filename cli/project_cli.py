# cli/project_cli.py

from services.project_service import (
    create_project,
    load_projects,
    assign_user_to_project,
    user_has_project_access,
)
from services.user_service import load_users
from services.task_service import load_tasks
from utils.decorators import require_role
from cli.task_cli import update_task_status_action
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


@require_role('admin')
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


@require_role('admin')
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
            all_tasks = load_tasks()

            if user.role == "admin":
                user_projects = projects
                dashboard_title = "PROJECT DASHBOARD (Global View)"
            else:
                user_projects = [p for p in projects if user_has_project_access(p, user.id)]
                dashboard_title = "PROJECT DASHBOARD (Your Projects & Tasks)"

            if not user_projects:
                print("\n📭 No projects available to display.")
            else:
                if USE_RICH:
                    from rich.table import Table

                    table = Table(title=f"\n[bold underline]{dashboard_title}[/bold underline]", show_header=True, header_style="bold cyan")
                    table.add_column("Proj ID", justify="right", style="cyan")
                    table.add_column("Project Name", style="cyan")
                    table.add_column("Task ID", justify="right")
                    table.add_column("Task Title")
                    table.add_column("Status", style="magenta")
                    if user.role == "admin":
                        table.add_column("Assigned To")

                    for project in user_projects:
                        if user.role == "admin":
                            project_tasks = [t for t in all_tasks if t.project_id == project.id]
                        else:
                            project_tasks = [t for t in all_tasks if t.project_id == project.id and t.assigned_to == user.id]

                        if project_tasks:
                            for i, task in enumerate(project_tasks):
                                # Only show the project ID/Name on the first row for this project to group them visually
                                p_id = str(project.id) if i == 0 else ""
                                p_name = project.name if i == 0 else ""
                                
                                if user.role == "admin":
                                    table.add_row(p_id, p_name, str(task.id), task.title, task.status, str(task.assigned_to))
                                else:
                                    table.add_row(p_id, p_name, str(task.id), task.title, task.status)
                        else:
                            if user.role == "admin":
                                table.add_row(str(project.id), project.name, "-", "[yellow]No tasks[/yellow]", "-", "-")
                            else:
                                table.add_row(str(project.id), project.name, "-", "[yellow]No tasks[/yellow]", "-")
                    
                    console.print(table)
                    print("")
                else:
                    print(f"\n=== {dashboard_title} ===")
                    for project in user_projects:
                        print(f"\nProject: {project.name} (ID: {project.id})")
                        print(f"Description: {project.description}")

                        if user.role == "admin":
                            project_tasks = [t for t in all_tasks if t.project_id == project.id]
                        else:
                            project_tasks = [t for t in all_tasks if t.project_id == project.id and t.assigned_to == user.id]

                        if project_tasks:
                            for task in project_tasks:
                                print(f"    -> Task: [{task.status}] {task.title} (Assigned to: {task.assigned_to})")
                        else:
                            print("    -> No tasks exist for this project." if user.role == "admin" else "    -> No tasks assigned to you for this project.")
                print("\n" + "=" * 45)
        elif choice == "4":
            update_task_status_action(session)
        elif choice == "5":
            break
        else:
            print("\n⚠️ Invalid project option selected.")