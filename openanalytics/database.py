import databases
import sqlalchemy
from alembic.config import Config as AlembicConfig
from alembic import command
from openanalytics.config import TESTING, DATABASE_URL, TEST_DATABASE_URL

metadata = sqlalchemy.MetaData()

if TESTING:
    database = databases.Database(TEST_DATABASE_URL)
else:
    database = databases.Database(DATABASE_URL)


async def run_migrations():
    alembic_cfg = AlembicConfig("alembic.ini")
    command.upgrade(alembic_cfg, "head")