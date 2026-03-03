from auth.session import Session
from auth import auth_service
from cli import menu
from cli import project_cli
from cli import task_cli

# load environment variables if .env exists
from dotenv import load_dotenv
load_dotenv()

def main():
    session = Session()

    print("Welcome to Teamflow CLI Task Management!")

    while True:
        if not session.is_authenticated():
            choice = menu.show_auth_menu()
            if choice == "login":
                # Assume these prompts are handled within the service or called separately
                username = input("Username: ")
                password = input("Password: ")
                if auth_service.login(username, password, session):
                    print(f"\nLogin successful! Welcome, {session.current_user.username}.")
                else:
                    print("\nLogin failed. Please check your credentials.")
            elif choice == "register":
                username = input("Username: ")
                password = input("Password: ")
                
                try:
                    auth_service.register(username, password, 'user')
                    print(f"\nRegistration successful for {username}! You can now login.")
                except ValueError as e:
                    print(f"\nError: {e}")
            elif choice == "exit":
                print("Goodbye!")
                break
            continue

        # Authenticated flow
        role = session.current_user.role
        if role == 'admin':
            choice, action_type = menu.show_admin_menu()
        else:
            choice, action_type = menu.show_user_menu()

        if choice == "logout":
            session.logout()
            print("Logged out successfully.")
            continue
        elif choice == "exit":
            print("Goodbye!")
            break

        # Route the choice
        if action_type == "project":
            project_cli.handle_project_actions(session)
        elif action_type == "task":
            task_cli.handle_task_actions(session)

if __name__ == "__main__":
    main()
