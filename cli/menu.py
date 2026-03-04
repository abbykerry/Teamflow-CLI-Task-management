# cli/menu.py

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
    print("1. Global Dashboard (Projects & Tasks)")
    print("2. Manage Projects")
    print("3. Manage Tasks")
    print("4. Logout")
    print("5. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        return "1", "dashboard"
    elif choice == "2":
        return "2", "manage_projects"
    elif choice == "3":
        return "3", "manage_tasks"
    elif choice == "4":
        return "logout", None
    elif choice == "5":
        return "exit", None
    else:
        print("Invalid choice.")
        return show_admin_menu()


def show_user_menu():
    print("\n=== USER MENU ===")
    print("1. My Dashboard (Projects & Tasks)")
    print("2. Update My Task Status")
    print("3. Logout")
    print("4. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        return "1", "dashboard"
    elif choice == "2":
        return "2", "update_task"
    elif choice == "3":
        return "logout", None
    elif choice == "4":
        return "exit", None
    else:
        print("Invalid choice.")
        return show_user_menu()


def admin_manage_projects_menu():
    print("\n=== MANAGE PROJECTS ===")
    print("1. Create New Project")
    print("2. Edit Project Details")
    print("3. Remove User from Project")
    print("4. Back")
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