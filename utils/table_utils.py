# utils/table_utils.py

"""Helper functions for printing beautifully formatted tables using rich.

This module provides ``display_table()`` which renders elegant, well-formatted
tables with rich styling, borders, and colors. All data is displayed in a
structured, scannable table format with clear column and row separation.
"""

from __future__ import annotations

from typing import Iterable, List, Any

from rich.console import Console
from rich.table import Table

_console = Console()


def display_table(
    title: str,
    headers: List[str],
    rows: Iterable[Iterable[Any]],
    header_style: str = "bold bright_white on dark_blue",
) -> None:
    """Print a beautifully formatted table using rich.

    ``title`` is displayed as a bold, underlined heading above the table.
    ``headers`` define the column names. ``rows`` should be an iterable of
    iterables where each inner iterable is a row. All values are converted to
    strings automatically.

    The table uses rich's sophisticated formatting with:
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

    # Add rows with alternating background for readability
    for i, row in enumerate(str_rows):
        # Alternate row colors for clarity
        row_style = "dim white on rgb(40,50,60)" if i % 2 == 0 else "white"
        table.add_row(*row, style=row_style)

    # Print with spacing
    _console.print()
    _console.print(table)
    _console.print()
