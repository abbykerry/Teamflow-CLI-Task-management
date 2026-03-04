# cli/project_cli.py

from services.project_service import (
    create_project,
    load_projects,
    assign_user_to_project,
    user_has_project_access,
    update_project,
    remove_user_from_project,
)
from services.user_service import load_users
from services.task_service import load_tasks, update_task, unassign_task
from utils.decorators import require_role
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
def edit_project_action(session):
    projects = load_projects()
    if not projects:
        print("\n⚠️ No projects exist yet.")
        return
        
    print("\n=== AVAILABLE PROJECTS ===")
    for p in projects:
        print(f"ID: {p.id} | Name: {p.name}")

    try:
        project_id = int(input("\nEnter project ID to edit: ").strip())
        name = input("Enter new name (leave blank to keep current): ").strip()
        desc = input("Enter new description (leave blank to keep current): ").strip()
        
        name = name if name else None
        desc = desc if desc else None
        
        if name is None and desc is None:
            print("\n⚠️ No changes requested.")
            return
        
        if update_project(project_id, name, desc):
            print(f"\n✅ Project {project_id} updated successfully.")
        else:
            print(f"\n❌ Project {project_id} not found.")
    except ValueError:
        print("\n❌ Error: IDs must be integers.")


@require_role('admin')
def remove_user_action(session):
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

    try:
        project_id = int(input("\nEnter project ID: ").strip())
        project = next((p for p in projects if p.id == project_id), None)
        if not project:
            print(f"\n❌ Project {project_id} not found.")
            return

        if not project.member_ids:
            print(f"\n⚠️ Project '{project.name}' has no members to remove.")
            return

        users = load_users()
        members = [u for u in users if u.id in project.member_ids]

        if USE_RICH:
            console.print(f"\n[bold underline]MEMBERS OF '{project.name.upper()}'[/bold underline]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("User ID", justify="right")
            table.add_column("Username")
            for m in members:
                table.add_row(str(m.id), m.username)
            console.print(table)
        else:
            print(f"\n=== MEMBERS OF PROJECT: {project.name} ===")
            for m in members:
                print(f"ID: {m.id} | Username: {m.username}")

        user_id = int(input("\nEnter user ID to remove: ").strip())

        if remove_user_from_project(project_id, user_id):
            # Also unassign any tasks belonging to this user in this project
            tasks = load_tasks()
            for t in tasks:
                if t.project_id == project_id and t.assigned_to == user_id:
                    unassign_task(t.id)
            print(f"\n✅ User {user_id} removed from project {project_id} and their tasks unassigned.")
        else:
            print(f"\n❌ Project {project_id} not found or user is not a member.")
    except ValueError:
        print("\n❌ Error: IDs must be integers.")


def view_dashboard_action(session):
    user = session.current_user
    projects = load_projects()
    all_tasks = load_tasks()
    users = load_users()
    user_map = {u.id: u.username for u in users}

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
                        
                        assigned_name = user_map.get(task.assigned_to, "Unknown")

                        if user.role == "admin":
                            table.add_row(p_id, p_name, str(task.id), task.title, task.status, assigned_name)
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
                        assigned_name = user_map.get(task.assigned_to, "Unknown")
                        print(f"    -> Task: [{task.status}] {task.title} (Assigned to: {assigned_name})")
                else:
                    print("    -> No tasks exist for this project." if user.role == "admin" else "    -> No tasks assigned to you for this project.")
        print("\n" + "=" * 45)


@require_role('admin')
def handle_manage_projects(session):
    """
    Handles project management routing for Admins.
    """
    while True:
        choice = menu.admin_manage_projects_menu()

        if choice == "1":
            create_project_action(session)
        elif choice == "2":
            edit_project_action(session)
        elif choice == "3":
            remove_user_action(session)
        elif choice == "4":
            break
        else:
            print("\n⚠️ Invalid option selected.")