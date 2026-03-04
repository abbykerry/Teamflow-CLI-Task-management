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
    print("1. Create project (Admin)")
    print("2. Assign user to project (Admin)")
    print("3. View my projects (Dashboard)")
    print("4. Update Task Status")
    print("5. Back")

    return input("Choose an option: ").strip()


def tasks_menu():
    print("\n=== TASKS MENU ===")
    print("1. Create Task (Admin)")
    print("2. Update Task Status")
    print("3. View My Tasks")
    print("4. View All Tasks (Admin)")
    print("5. Reassign Task (Admin)")
    print("6. Back")

    return input("Choose an option: ").strip()