# Teamflow CLI Task Management

This repository implements a simple command-line task and project management
application written in **Python 3**. The design emphasizes clean separation of
concerns, persistence via JSON files, and a familiar CRUD-style user
experience. It was originally built as part of an educational exercise and has
been incrementally enhanced to demonstrate good software engineering practices
including encapsulation, dependency management, logging, and thorough testing.

## Features

- User authentication with roles (`admin` or `user`)
- Create/read/update/delete projects and tasks
- Assign tasks to users and mark them complete
- Persistence to JSON files under a configurable `DATA_DIR`
- Optional rich-formatted tables when the `rich` package is installed
- Environment configuration via `.env` and `python-dotenv`
- Logging with per-module loggers and adjustable levels via `LOG_LEVEL`

## Project Layout

```
Teamflow-CLI-Task-management/
│
├── cli/                 # command-line interface modules
├── models/              # data classes (User, Project, Task) with validation
├── services/            # business logic and persistence functions
├── utils/               # helper utilities (logging, etc.)
├── tests/               # pytest-compatible unit tests
├── data/                # default data directory for JSON files
├── Pipfile              # dependency management via Pipenv
└── README.md            # this document
```

## Requirements & Setup

1. Install Python 3.10 or newer.
2. Clone the repository and `cd` into it.
3. Install the required dependencies using `pipenv`:

	```sh
	pipenv install
	```

4. Since the database files (`data/*.json`) are excluded from version control, you **must** initialize a clean, local database before running the app. Do this by running:

	```sh
	python3 setup_users.py
	```
	*This will create the necessary data files along with a fresh Admin account.*

5. Run the CLI with one of the following (both are equivalent):

    ```sh
    python3 -m cli.main
    # or
    python -m cli.main
    ```

    The application uses the `rich` package to render beautiful tables where
    available; if `rich` is not installed an ASCII-style table will still be
    printed so every list remains formatted in a tabular layout.

## Encapsulation and Validation

The `models` package exposes classes (`User`, `Project`, `Task`) whose
attributes are private and accessed via properties. Setters validate input and
raise `ValueError` on invalid usage, aiding correctness when services or CLI
code interact with them.

## Logging

All modules acquire loggers from `utils/logger.py`. The level is controlled by
`LOG_LEVEL` environment variable and defaults to `INFO`. This makes debugging
and auditing operations easier.

## Testing

Unit tests live under the `tests/` directory and exercise service functions and
file persistence. Temporary directories are used to avoid mutating real data.

Run the tests with `pytest`:

```sh
pytest -q
```

## Contributing

Feel free to fork the repository and submit pull requests. Follow the existing
style of simple functions, clear docstrings, and keep logic in services rather
than CLI modules.

## License

This project is provided under the MIT License. See `LICENSE.md` for details.