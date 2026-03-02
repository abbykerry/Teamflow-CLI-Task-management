# cli/task_cli.py

from services.task_service import create_task, load_tasks
from services.project_service import load_projects
from services.user_service import load_users
from cli import menu


def handle_task_actions(session):
    """
    Handles task-related actions by showing the tasks sub-menu.
    Control returns to main.py after this function finishes.
    """

    user = session.current_user  # logged-in user object
    
    # Get user choice from the sub-menu
    choice = menu.tasks_menu()

    # OPTION 1: Create task
    if choice == "1":
        # Step 1: Check and display projects
        projects = load_projects()
        if not projects:
            print("\n⚠️ Warning: No projects exist. Please create a project first.")
            return

        print("\n=== AVAILABLE PROJECTS ===")
        for project in projects:
            print(f"ID: {project.id} | Name: {project.name}")

        while True:
            try:
                project_id_input = input("\nEnter project ID: ").strip()
                project_id = int(project_id_input)
                break
            except ValueError:
                print("Error: Invalid Project ID. Please enter a valid integer.")

        # Step 2: Check and display users
        users = load_users()
        print("\n=== AVAILABLE USERS ===")
        for u in users:
            print(f"ID: {u.id} | Username: {u.username} | Role: {u.role}")

        while True:
            try:
                assigned_to_input = input("\nEnter the User ID to assign this task to: ").strip()
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

        print(
            f"\n✅ Task '{new_task.title}' created successfully "
            f"(ID: {new_task.id})"
        )

    # OPTION 2: View my tasks
    elif choice == "2":
        tasks = load_tasks()

        user_tasks = [
            t for t in tasks if t.assigned_to == user.id
        ]

        if not user_tasks:
            print("\n📭 You have no tasks assigned.")
        else:
            print("\n=== YOUR TASKS ===")
            for task in user_tasks:
                print(
                    f"ID: {task.id} | "
                    f"Project ID: {task.project_id} | "
                    f"Title: {task.title} | "
                    f"Status: {task.status}"
                )

    # Back to main menu
    elif choice == "3":
        return

    else:
        print("\n⚠️ Invalid task option selected.")