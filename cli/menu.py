# cli/menus.py

def show_auth_menu():
    print("\n=== AUTH MENU ===")
    print("1. Login")
    print("2. Register")
    print("3. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        return "login"
    elif choice == "2":
        return "register"
    elif choice == "3":
        return "exit"
    else:
        print("Invalid choice.")
        return show_auth_menu()


def show_admin_menu():
    print("\n=== ADMIN MENU ===")
    print("1. Projects")
    print("2. Tasks")
    print("3. Logout")
    print("4. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        return "1", "project"
    elif choice == "2":
        return "2", "task"
    elif choice == "3":
        return "logout", None
    elif choice == "4":
        return "exit", None
    else:
        print("Invalid choice.")
        return show_admin_menu()


def show_user_menu():
    print("\n=== USER MENU ===")
    print("1. My Projects")
    print("2. My Tasks")
    print("3. Logout")
    print("4. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        return "1", "project"
    elif choice == "2":
        return "2", "task"
    elif choice == "3":
        return "logout", None
    elif choice == "4":
        return "exit", None
    else:
        print("Invalid choice.")
        return show_user_menu()


def projects_menu():
    print("\n=== PROJECTS MENU ===")
    print("1. Create project")
    print("2. View my projects")
    print("3. Back")

    return input("Choose an option: ").strip()


def tasks_menu():
    print("\n=== TASKS MENU ===")
    print("1. Create Task")
    print("2. View Tasks")
    print("3. Back")

    return input("Choose an option: ").strip()