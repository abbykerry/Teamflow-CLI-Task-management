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

    # Ask if admin wants to assign now or leave unassigned
    assigned_to = None
    assign_now = input("\nAssign this task now? (y/N): ").strip().lower()
    if assign_now == 'y':
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
                assigned_to_input = input("\nEnter the User ID to assign this task to: ").strip()
                if assigned_to_input == "":
                    assigned_to = None
                    break
                assigned_to = int(assigned_to_input)
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
    if assigned_to is not None:
        assign_user_to_project(project_id, assigned_to)

    print(f"\n✅ Task '{new_task.title}' created successfully (ID: {new_task.id})")


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

def handle_task_actions(session):
    """
    Handles task-related actions. Keeps showing the tasks menu until the user
    selects the "Back" option.
    """
    user = session.current_user
    while True:
        choice = menu.tasks_menu()

        if choice == "1":
            create_task_action(session)
        elif choice == "2":
            update_task_status_action(session)
        elif choice == "3":
            tasks = load_tasks()
            assigned_tasks = [t for t in tasks if t.assigned_to == user.id]

            if not assigned_tasks:
                print("\n📭 You have no tasks assigned.")
            else:
                if USE_RICH:
                    console.print("\n[bold underline]YOUR TASKS[/bold underline]")
                    table = Table(show_header=True, header_style="bold green")
                    table.add_column("ID", justify="right")
                    table.add_column("Project")
                    table.add_column("Title")
                    table.add_column("Status")
                    for task in assigned_tasks:
                        table.add_row(str(task.id), str(task.project_id), task.title, task.status)
                    console.print(table)
                else:
                    print("\n=== YOUR TASKS ===")
                    for task in assigned_tasks:
                        print(f"ID: {task.id} | Project ID: {task.project_id} | Title: {task.title} | Status: {task.status}")
        elif choice == "4":
            view_all_tasks_action(session)
        elif choice == "5":
            reassign_task_action(session)
        elif choice == "6":
            # return to previous menu
            break
        else:
            print("\n⚠️ Invalid task option selected.")