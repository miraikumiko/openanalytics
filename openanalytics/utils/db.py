import os
from pathlib import Path
from databases import DatabaseURL


def is_url(path: DatabaseURL) -> bool:
    return bool(path.hostname)


def is_absolute_path(path: str) -> bool:
    return Path(path).is_absolute()


def is_relative_path(path: str) -> bool:
    return path.startswith("./") or path.startswith("../") or not path.startswith("/")


def check_path_type(db_url: DatabaseURL) -> int:
    """0 — Memory, 1 — URL, 2 — Relative, 3 — Absolute, 4 — Unknown"""

    if db_url.database == ":memory:":
        return 0

    if is_url(db_url):
        return 1

    if is_relative_path(db_url.database):
        return 2

    if is_absolute_path(db_url.database):
        return 3

    return 4


def test_db_prefix(db_url: DatabaseURL) -> DatabaseURL:
    path_type = check_path_type(db_url)

    if path_type == 0:
        return db_url

    if path_type == 1:
        return db_url.replace(database="test_" + db_url.database)

    if path_type in (2, 3):
        db_schema = db_url.scheme
        base_path, db_name = os.path.split(str(db_url.database))
        test_db_name = "test_" + db_name

        return DatabaseURL(f"{db_schema}:///{base_path}/{test_db_name}")

    raise ValueError("Invalid Database URL")
