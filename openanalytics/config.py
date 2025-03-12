from starlette.config import Config
from databases import DatabaseURL

config = Config("/etc/openanalytics.conf")

TESTING = config("TESTING", cast=bool, default=False)

HOST = config("HOST", default="127.0.0.1")
PORT = config("PORT", cast=int, default=8000)

DATABASE_URL = config("DATABASE_URL", cast=DatabaseURL, default=DatabaseURL("sqlite:///usr/lib/openanalytics/openanalytics.db"))
TEST_DATABASE_URL = DATABASE_URL.replace(database="test_" + DATABASE_URL.database)