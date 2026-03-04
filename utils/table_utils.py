# utils/table_utils.py

"""Helper functions for printing tabular data consistently.

This module provides a single entrypoint, ``display_table``. It will use
``rich`` when available to render a beautiful table; if ``rich`` is not
installed it falls back to a minimal ASCII-style table.  Using this helper
ensures that all CLI views look like tables regardless of the environment.

The design keeps the dependency optional so the package remains lightweight, but
users are encouraged to ``pip install rich`` for the enhanced experience.
"""

from __future__ import annotations

from typing import Iterable, List, Any

try:
    from rich.console import Console
    from rich.table import Table
    _RICH_AVAILABLE = True
    _console = Console()
except ImportError:  # pragma: no cover - cannot easily simulate absence
    _RICH_AVAILABLE = False
    _console = None


def display_table(
    title: str,
    headers: List[str],
    rows: Iterable[Iterable[Any]],
    header_style: str = "bold cyan",
) -> None:
    """Print a table with the given ``headers`` and ``rows``.

    ``title`` is a short string that will be shown above the table.  ``rows``
    should be an iterable of iterables, each item corresponding to a row and
    each element in the row corresponding to a column.  Values will be
    converted to :class:`str` automatically.

    When ``rich`` is present the table is rendered via ``rich.table.Table``; if
    not, a plain ASCII table with separators is printed instead.
    """

    # Convert rows to strings immediately so that we can compute column widths
    str_rows = [[str(item) for item in row] for row in rows]

    if _RICH_AVAILABLE:
        _console.print(f"\n[bold underline]{title}[/bold underline]")
        table = Table(show_header=True, header_style=header_style)
        for h in headers:
            table.add_column(h)
        for row in str_rows:
            table.add_row(*row)
        _console.print(table)
    else:
        # ascii fallback
        # compute max width for each column
        widths = [len(h) for h in headers]
        for row in str_rows:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(cell))
                else:
                    widths.append(len(cell))
        sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
        header_row = "|" + "|".join(f" {headers[i].ljust(widths[i])} " for i in range(len(headers))) + "|"

        print(f"\n{title}")
        print(sep)
        print(header_row)
        print(sep)
        for row in str_rows:
            row_line = "|" + "|".join(
                f" {row[i].ljust(widths[i])} " if i < len(row) else f" {'':{widths[i]}} "
                for i in range(len(widths))
            ) + "|"
            print(row_line)
        print(sep)
