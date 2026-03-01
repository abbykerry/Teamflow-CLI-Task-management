from cli.menus import main_menu, projects_menu
from services.project_service import create_project, load_projects

def run_cli(): #this is the main function that runs the CLI application
    while True:
        choice = main_menu() #calls the main_menu function to display the menu and get user input

        if choice == "1":
            while True:
                project_choice = projects_menu()

                if project_choice == "1":
                    name = input("Enter project name: ").strip()
                    description = input("Enter project description: ").strip()
                    # Example: assume current user is owner with id=1 for now
                    owner_id = 1
                    new_project = create_project(name, description, owner_id)
                    print(f"Project '{new_project.name}' created successfully with ID {new_project.id}!")

                elif project_choice == "2":
                    projects = load_projects()

                    # Temporary: only show projects owned by current user (id=1 for now)
                    owner_id = 1
                    user_projects = [p for p in projects if p.owner_id == owner_id]

                    if not user_projects:
                        print("You have no projects yet.")
                    else:
                        print("\n=== YOUR PROJECTS ===")
                        for p in user_projects:
                            print(f"ID: {p.id}, Name: {p.name}, Description: {p.description}")
                elif project_choice == "3":
                        break
                else:
                    print("Invalid choice, try again.")
        elif choice == "2":
            print("Tasks menu coming soon...")
        elif choice == "3":
            print("Logging out...")
            break
        elif choice == "4":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice, try again.")