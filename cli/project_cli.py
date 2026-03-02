# cli/project_cli.py

from services.project_service import create_project, load_projects


def handle_project_actions(choice, session):
    """
    Handles ONE project-related action based on the user's menu choice.
    Control always returns to main.py after this function finishes.
    """

    user = session.current_user  # logged-in user object

    # OPTION 1: Create project
    if choice == "1":
        name = input("Enter project name: ").strip()
        description = input("Enter project description: ").strip()

        new_project = create_project(
            name=name,
            description=description,
            owner_id=user.id
        )

        print(
            f"\n✅ Project '{new_project.name}' created successfully "
            f"(ID: {new_project.id})"
        )

    # OPTION 2: View my projects
    elif choice == "2":
        projects = load_projects()

        user_projects = [
            p for p in projects if p.owner_id == user.id
        ]

        if not user_projects:
            print("\n📭 You have no projects yet.")
        else:
            print("\n=== YOUR PROJECTS ===")
            for project in user_projects:
                print(
                    f"ID: {project.id} | "
                    f"Name: {project.name} | "
                    f"Description: {project.description}"
                )

    # Any other choice (defensive programming)
    else:
        print("\n⚠️ Invalid project option selected.")