# cli/task_cli.py

from services.task_service import create_task, load_tasks


def handle_task_actions(choice, session):
    """
    Handles ONE task-related action based on the user's menu choice.
    Control always returns to main.py after this function finishes.
    """

    user = session.current_user  # logged-in user object

    # OPTION 1: Create task
    if choice == "1":
        project_id = input("Enter project ID: ").strip()
        title = input("Enter task title: ").strip()

        # Optional assignment: default to current user
        assigned_to = user.id

        new_task = create_task(
            project_id=int(project_id),
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

    else:
        print("\n⚠️ Invalid task option selected.")