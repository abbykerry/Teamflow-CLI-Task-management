def main_menu():
    print("\n=== MAIN MENU ===") #adds a newline before the menu for better readability
    print("1. Projects")
    print("2. Tasks")
    print("3. Logout")
    print("4. Exit")

    choice = input("Choose an option: ").strip()
    return choice

def projects_menu():
    print("\n=== PROJECTS MENU ===")
    print("1. Create project")
    print("2. View my projects")
    print("3. Back")

    choice = input("Choose an option: ").strip()
    return choice