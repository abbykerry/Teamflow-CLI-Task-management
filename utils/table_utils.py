# utils/table_utils.py

"""Helper functions for printing beautifully formatted tables using rich.

This module provides ``display_table()`` which renders elegant, well-formatted
tables with rich styling, borders, and colors. All data is displayed in a
structured, scannable table format with clear column and row separation.
"""

from __future__ import annotations #this allows us to use the function name in its own type hints. 
#type hints is a way to indicate the expected data types of function arguments and return values, 
# which can help with code readability and debugging.

from typing import Iterable, List, Any

from rich.console import Console
from rich.table import Table

_console = Console()

#Implemented this function so that we can use it across the CLI to display tables of projects,
# users, and tasks in a consistent, visually appealing way.
def display_table(
    title: str,
    headers: List[str],
    rows: Iterable[Iterable[Any]],
    header_style: str = "bold bright_white on dark_blue",
) -> None:
    """Prints a formatted table using rich.
    The table uses rich's formatting with:
    - Distinct borders and row separators
    - Colored, styled headers
    - Proper column alignment
    - Padding for readability
    """

    # Convert rows to strings
    str_rows = [[str(item) for item in row] for row in rows]

    # Create table with clean, distinct styling
    table = Table(
        title=f"[bold bright_white]{title}[/bold bright_white]",
        show_header=True,
        header_style=header_style,
        border_style="cyan",
        padding=(0, 1),
        show_lines=True,  # Add horizontal lines between rows for clarity
    )

    # Add columns
    for h in headers:
        table.add_column(h, style="white")

    # Add rows with alternating background for readability. This is actually so cool!
    # We use a dimmed style for even rows and a normal style for odd rows to create a zebra-striping effect.
    for i, row in enumerate(str_rows):
        # Alternate row colors for clarity
        row_style = "dim white on rgb(40,50,60)" if i % 2 == 0 else "white"
        table.add_row(*row, style=row_style)

    # Print with spacing
    #here we are adding extra spacing before and after the table to ensure it stands out and is visually separated from other content in the CLI.
    #console comes from rich library, it's an object. It handles the actual rendering of the table to the terminal.
    _console.print()
    _console.print(table)
    _console.print()
