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

# optional rich support for pretty tables; unified rendering via helper
from utils.table_utils import display_table

# keep USE_RICH flag for backward compatibility
try:
    from rich.console import Console  # noqa: F401
    USE_RICH = True
except ImportError:
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

    headers = ["ID", "Name"]
    rows = [[str(p.id), p.name] for p in projects]
    display_table("AVAILABLE PROJECTS", headers, rows)

    # Show users
    users = load_users()
    headers = ["ID", "Username", "Role"]
    rows = [[str(u.id), u.username, u.role] for u in users]
    display_table("AVAILABLE USERS", headers, rows)

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
                # prepare table headers and rows regardless of rich availability
                if user.role == "admin":
                    headers = ["Proj ID", "Project Name", "Task ID", "Task Title", "Status", "Assigned To"]
                else:
                    headers = ["Proj ID", "Project Name", "Task ID", "Task Title", "Status"]

                rows = []
                for project in user_projects:
                    if user.role == "admin":
                        project_tasks = [t for t in all_tasks if t.project_id == project.id]
                    else:
                        project_tasks = [t for t in all_tasks if t.project_id == project.id and t.assigned_to == user.id]

                    if project_tasks:
                        for i, task in enumerate(project_tasks):
                            p_id = str(project.id) if i == 0 else ""
                            p_name = project.name if i == 0 else ""
                            assigned_name = user_map.get(task.assigned_to, "Unknown")
                            if user.role == "admin":
                                rows.append([p_id, p_name, str(task.id), task.title, task.status, assigned_name])
                            else:
                                rows.append([p_id, p_name, str(task.id), task.title, task.status])
                    else:
                        if user.role == "admin":
                            rows.append([str(project.id), project.name, "-", "No tasks", "-", "-"])
                        else:
                            rows.append([str(project.id), project.name, "-", "No tasks", "-"])

                display_table(dashboard_title, headers, rows)
                print("\n" + "=" * 45)
        elif choice == "4":
            update_task_status_action(session)
        elif choice == "5":
            break
        else:
            print("\n⚠️ Invalid project option selected.")