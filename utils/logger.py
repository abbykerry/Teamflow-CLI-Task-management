import logging
import os

"""Simple logging helper for the Teamflow CLI application.

The module configures the root logger once and exposes a
`get_logger(name)` convenience function so each submodule can
obtain a properly named logger.
"""

# configure logging via environment variable
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_logger(name: str):
    """Return a logger configured with the shared format and level.

    Args:
        name: The name of the subsystem (e.g., 'user_service').
    """
    return logging.getLogger(name)


# convenience root logger in case someone prefers a default name
logger = get_logger("teamflow")
