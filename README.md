A CLI task management system for teams
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
3. (Recommended) Use `pipenv` or another virtual environment:

	```sh
	pipenv install --dev
	pipenv shell
	```

4. Populate optional environment variables in a `.env` file:

	```env
	DATA_DIR=data      # path where JSON files will be stored
	LOG_LEVEL=DEBUG   # logging verbosity
	```

5. Run the CLI with:

	```sh
	python main.py
	```

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
A CLI task management system for teams
