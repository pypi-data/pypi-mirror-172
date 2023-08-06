"""a few links"""

from os import environ
from .exceptions import MustBeOnReplit


class links:
    """bot urls (docs)"""

    if (
        "REPL_SLUG" not in environ
        or "REPL_OWNER" not in environ
        or "REPLIT_DB_URL" not in environ
    ):
        raise MustBeOnReplit(
            "Currently, you must be on replit to run this. Thanks! Local support is WIP"
        )
    docs: str = f"https://{environ['REPL_SLUG']}.{environ['REPL_OWNER']}.repl.co"
