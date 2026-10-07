"""Initialize SQLite database"""

import os
from pathlib import Path
from sqlite3 import (
    Connection,
    Cursor,
    IntegrityError,  # noqa: F401
    connect,
)

conn: Connection | None = None
curs: Cursor
transaction: Connection


def get_db(name: str | None = None, reset: bool = False):
    """Connect to SQLite database file"""
    global conn, curs, transaction
    if conn:
        if not reset:
            return
        conn = None
    if not name:
        # name = os.getenv("CRYPTID_SQLITE_DB")
        top_dir = Path(__file__).resolve().parents[1]  # repo top
        db_dir = top_dir / "db"
        db_dir.mkdir(parents=True, exist_ok=True)  # dir needs to exist to create db
        db_name = "cryptid.db"
        db_path = str(db_dir / db_name)
        name = os.getenv("CRYPTID_SQLITE_DB", db_path)
    conn = connect(name, check_same_thread=False)
    curs = conn.cursor()
    # Better name for commiting transactions
    transaction = conn


get_db()
