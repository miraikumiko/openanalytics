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
    """0 — URL, 1 — Relative, 2 — Absolute, 3 — Unknown"""

    if is_url(db_url):
        return 0
    elif is_relative_path(db_url.database):
        return 1
    elif is_absolute_path(db_url.database):
        return 2
    else:
        return 3


def test_db_prefix(db_url: DatabaseURL) -> DatabaseURL:
    path_type = check_path_type(db_url)

    if path_type == 0:
        return db_url.replace(database="test_" + db_url.database)
    elif path_type == 1 or path_type == 2:
        db_schema = db_url.scheme
        base_path, db_name = os.path.split(str(db_url.database))
        test_db_name = "test_" + db_name

        return DatabaseURL(f"{db_schema}:///{base_path}/{test_db_name}")
    else:
        raise Exception("Invalid Database URL")
