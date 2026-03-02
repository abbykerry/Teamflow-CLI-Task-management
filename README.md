# Teamflow CLI

Teamflow CLI is a modular, object-oriented task management system designed for organizational project tracking and team assignments. It features local JSON persistence and a robust role-based security model.

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/abbykerry/Teamflow-CLI-Task-management.git
   cd Teamflow-CLI-Task-management
   ```

2. Install required dependencies:
   ```bash
   pip install rich
   ```

3. Execute the application:
   ```bash
   python3 -m cli.main
   ```

---

## Core Features and Role-Based Access Control (RBAC)

The system implements a structured permission model to maintain data integrity and organizational security.

- **Authentication**: Secure registration and login protocols utilizing PBKDF2-HMAC-SHA256 password hashing with unique salts.
- **Admin Privileges**:
  - Authorized to initialize and manage projects.
  - Capability to assign tasks to any team member within the system.
  - Full visibility into global project and user states.
- **User Privileges**:
  - Restricted access to view only owned or specifically assigned projects.
  - Ability to monitor and update the status of personally assigned tasks.

---

## Technical Architecture

The application is built on a defensible design emphasizing modularity and standard software engineering principles.

### Modular Layering
- **Models**: Defines core data structures (User, Project, Task) using Python classes for clear data representation.
- **Services**: Manages business logic and the persistence layer, including JSON serialization and deserialization.
- **CLI**: The presentation layer, responsible for user interaction, sub-menu routing, and input validation.

### Object-Oriented Programming (OOP) Principles
- **Inheritance**: Utilizes a logical hierarchy where the `User` class inherits from a base `Person` class, facilitating code reuse.
- **Encapsulation**: Protected data, such as `_password_hash`, is managed through `@property` decorators and setters to prevent unauthorized direct access.

### Session and Security Management
- **Session Management**: A dedicated `Session` class functions as a global state manager, maintaining authenticated user identity and role context across nested sub-menus.
- **Security Decorators**: Custom `@require_role` decorators intercept function calls at the CLI layer, enforcing access control before any underlying business logic is executed.

---

## Testing

To verify the security and reliability of the authentication and logic layers, execute the unit test suite:

```bash
python3 -m unittest tests/test_auth.py
```

---

## Project Management

Development followed an Agile methodology, utilizing a Kanban-based workflow to manage Git feature branches and ensure compliance with technical requirements.
