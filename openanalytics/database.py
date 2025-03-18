import asyncpg
from databases import Database, DatabaseURL
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from openanalytics.config import TESTING, DATABASE_URL, TEST_DATABASE_URL

metadata = MetaData()

if TESTING:
    database = Database(TEST_DATABASE_URL)
else:
    database = Database(DATABASE_URL)


async def run_migrations(url: DatabaseURL):
    conn = await asyncpg.connect(
        user=url.username,
        password=url.password,
        database="postgres",
        host=url.hostname
    )

    databases = await conn.fetch("SELECT datname FROM pg_database")
    db_names = [db["datname"] for db in databases]

    if url.database not in db_names:
        await conn.execute(f"CREATE DATABASE {url.database}")

    engine = create_async_engine(str(url))

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    await conn.close()


async def drop_database(url: DatabaseURL):
    conn = await asyncpg.connect(
        user=url.username,
        password=url.password,
        database="postgres",
        host=url.hostname
    )

    databases = await conn.fetch("SELECT datname FROM pg_database")
    db_names = [db["datname"] for db in databases]

    if url.database in db_names:
        await conn.execute(f"DROP DATABASE {url.database}")

    await conn.close()
    await database.disconnect()
