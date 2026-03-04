# cli/task_cli.py

from services.task_service import create_task, load_tasks, save_tasks, update_task_assignment
from services.project_service import load_projects, assign_user_to_project
from services.user_service import load_users, get_user_by_id
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
def create_task_action(session):
    """Display projects and users, then create a task (admin-only via menu guard)."""
    projects = load_projects()
    if not projects:
        print("\n⚠️ Warning: No projects exist. Please create a project first.")
        return

    if USE_RICH:
        console.print("\n[bold underline]AVAILABLE PROJECTS[/bold underline]")
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID", justify="right")
        table.add_column("Name")
        for project in projects:
            table.add_row(str(project.id), project.name)
        console.print(table)
    else:
        print("\n=== AVAILABLE PROJECTS ===")
        for project in projects:
            print(f"ID: {project.id} | Name: {project.name}")

    while True:
        try:
            project_id = int(input("\nEnter project ID: ").strip())
            break
        except ValueError:
            print("Error: Invalid Project ID. Please enter a valid integer.")

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

    while True:
        try:
            assigned_to = int(input("\nEnter the User ID to assign this task to: ").strip())
            break
        except ValueError:
            print("Error: Invalid User ID. Please enter a valid integer.")

    title = input("Enter task title: ").strip()

    new_task = create_task(
        project_id=project_id,
        title=title,
        assigned_to=assigned_to
    )

    # Automatically enroll the user into the project when assigned a task
    assign_user_to_project(project_id, assigned_to)

    print(f"\n✅ Task '{new_task.title}' created successfully (ID: {new_task.id})")


@require_role('admin')
def edit_task_action(session):
    tasks = load_tasks()
    if not tasks:
        print("\n⚠️ No tasks exist yet.")
        return

    if USE_RICH:
        console.print("\n[bold underline]AVAILABLE TASKS[/bold underline]")
        table = Table(show_header=True, header_style="bold green")
        table.add_column("ID", justify="right")
        table.add_column("Project", justify="right")
        table.add_column("Title")
        table.add_column("Status")
        table.add_column("Assignee", justify="right")
        for t in tasks:
            table.add_row(str(t.id), str(t.project_id), t.title, t.status, str(t.assigned_to))
        console.print(table)
    else:
        print("\n=== AVAILABLE TASKS ===")
        for t in tasks:
            print(f"ID: {t.id} | Proj: {t.project_id} | Title: {t.title} | Status: {t.status} | Assignee: {t.assigned_to}")

    try:
        task_id = int(input("\nEnter task ID to edit: ").strip())
        
        # Display available statuses
        print("\nAvailable statuses:")
        print("1. todo")
        print("2. in_progress")
        print("3. done")
        print("4. (Keep current)")
        status_choice = input("Choose a status option (1-4): ").strip()
        status_map = {"1": "todo", "2": "in_progress", "3": "done"}
        status = status_map.get(status_choice, None)
        
        title = input("Enter new title (leave blank to keep current): ").strip()
        title = title if title else None

        users = load_users()
        if USE_RICH:
            console.print("\n[bold underline]AVAILABLE USERS (For Reassignment)[/bold underline]")
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

        assign_input = input("\nEnter new assignee ID (leave blank to keep current): ").strip()
        assigned_to = int(assign_input) if assign_input else None
        
        if status is None and title is None and assigned_to is None:
            print("\n⚠️ No changes requested.")
            return

        if update_task(task_id, title=title, assigned_to=assigned_to, status=status):
            print(f"\n✅ Task {task_id} updated successfully.")
            if assigned_to is not None:
                # Find task to get its project ID so we can auto-enroll the new assignee
                updated_t = next((t for t in load_tasks() if t.id == task_id), None)
                if updated_t:
                    assign_user_to_project(updated_t.project_id, assigned_to)
        else:
            print(f"\n❌ Task {task_id} not found.")

    except ValueError:
        print("\n❌ Error: Invalid input. Expected an integer where applicable.")


@require_role('admin')
def delete_task_action(session):
    try:
        task_id = int(input("\nEnter task ID to delete: ").strip())
        if delete_task(task_id):
            print(f"\n✅ Task {task_id} deleted successfully.")
        else:
            print(f"\n❌ Task {task_id} not found.")
    except ValueError:
        print("\n❌ Error: IDs must be integers.")


def update_task_status_action(session):
    """Update status of a task assigned to the current user"""
    user = session.current_user
    tasks = load_tasks()
    user_tasks = [t for t in tasks if t.assigned_to == user.id]

    if not user_tasks:
        print("\n📭 You have no tasks assigned.")
        return

    if USE_RICH:
        console.print("\n[bold underline]YOUR TASKS[/bold underline]")
        table = Table(show_header=True, header_style="bold green")
        table.add_column("ID", justify="right")
        table.add_column("Project")
        table.add_column("Title")
        table.add_column("Status")
        for task in user_tasks:
            table.add_row(str(task.id), str(task.project_id), task.title, task.status)
        console.print(table)
    else:
        print("\n=== YOUR TASKS ===")
        for task in user_tasks:
            print(f"ID: {task.id} | Project ID: {task.project_id} | Title: {task.title} | Status: {task.status}")

    try:
        task_id = int(input("\nEnter task ID to update status: ").strip())
        # Find the specific task
        target_task = next((t for t in user_tasks if t.id == task_id), None)
        
        if target_task:
            print("\nAvailable statuses:")
            print("1. todo")
            print("2. in_progress")
            print("3. done")
            
            status_choice = input("Choose an option (1-3): ").strip()
            status_map = {
                "1": "todo",
                "2": "in_progress",
                "3": "done"
            }
            
            if status_choice in status_map:
                new_status = status_map[status_choice]
                target_task.status = new_status
                save_tasks(tasks)
                print(f"\n✅ Task {task_id} status updated to '{new_status}'.")
            else:
                print("\n❌ Error: Invalid status option selected.")
        else:
            print(f"\n❌ You are not assigned to task ID {task_id}.")
    except ValueError:
        print("\n❌ Error: task ID must be an integer.")

@require_role('admin')
def view_all_tasks_action(session):
    """Display all tasks in the system with assignee information (admin-only)."""
    tasks = load_tasks()
    
    if not tasks:
        print("\n📭 No tasks exist in the system.")
        return
    
    # Get all users for name lookup
    users = load_users()
    user_map = {u.id: u.username for u in users}
    
    if USE_RICH:
        console.print("\n[bold underline]ALL TASKS[/bold underline]")
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("ID", justify="right")
        table.add_column("Project ID", justify="right")
        table.add_column("Title")
        table.add_column("Assigned To")
        table.add_column("Status")
        
        for task in tasks:
            assigned_user = user_map.get(task.assigned_to, "Unassigned") if task.assigned_to else "Unassigned"
            table.add_row(
                str(task.id),
                str(task.project_id),
                task.title,
                assigned_user,
                task.status
            )
        console.print(table)
    else:
        print("\n=== ALL TASKS ===")
        for task in tasks:
            assigned_user = user_map.get(task.assigned_to, "Unassigned") if task.assigned_to else "Unassigned"
            print(f"ID: {task.id} | Project: {task.project_id} | Title: {task.title} | Assigned To: {assigned_user} | Status: {task.status}")


@require_role('admin')
def reassign_task_action(session):
    """Reassign a task to a different user (admin-only)."""
    tasks = load_tasks()
    
    if not tasks:
        print("\n📭 No tasks exist in the system.")
        return
    
    # Get all users for name lookup
    users = load_users()
    user_map = {u.id: u.username for u in users}
    
    # Display all tasks
    if USE_RICH:
        console.print("\n[bold underline]ALL TASKS[/bold underline]")
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("ID", justify="right")
        table.add_column("Title")
        table.add_column("Currently Assigned To")
        table.add_column("Status")
        
        for task in tasks:
            assigned_user = user_map.get(task.assigned_to, "Unassigned") if task.assigned_to else "Unassigned"
            table.add_row(
                str(task.id),
                task.title,
                assigned_user,
                task.status
            )
        console.print(table)
    else:
        print("\n=== ALL TASKS ===")
        for task in tasks:
            assigned_user = user_map.get(task.assigned_to, "Unassigned") if task.assigned_to else "Unassigned"
            print(f"ID: {task.id} | Title: {task.title} | Assigned To: {assigned_user} | Status: {task.status}")
    
    # Get task ID to reassign
    try:
        task_id = int(input("\nEnter task ID to reassign: ").strip())
        target_task = next((t for t in tasks if t.id == task_id), None)
        
        if not target_task:
            print(f"\n❌ Task with ID {task_id} not found.")
            return
        
        # Display available users
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
        
        # Get new assignee
        new_assignee_id = int(input("\nEnter User ID to reassign this task to: ").strip())
        
        # Verify user exists
        if not get_user_by_id(new_assignee_id):
            print(f"\n❌ User with ID {new_assignee_id} does not exist.")
            return
        
        # Update the task assignment
        update_task_assignment(task_id, new_assignee_id)
        new_assignee_name = user_map.get(new_assignee_id, "Unknown")
        print(f"\n✅ Task '{target_task.title}' has been reassigned to {new_assignee_name}.")
        
    except ValueError:
        print("\n❌ Error: Please enter valid integer IDs.")

@require_role('admin')
def handle_manage_tasks(session):
    """
    Handles task management routing for Admins.
    """
    while True:
        choice = menu.admin_manage_tasks_menu()

        if choice == "1":
            create_task_action(session)
        elif choice == "2":
            edit_task_action(session)
        elif choice == "3":
            delete_task_action(session)
        elif choice == "4":
            view_all_tasks_action(session)
        elif choice == "5":
            reassign_task_action(session)
        elif choice == "6":
            # return to previous menu
            break
        else:
            print("\n⚠️ Invalid option selected.")