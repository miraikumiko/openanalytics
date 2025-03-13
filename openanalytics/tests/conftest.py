import pytest
from starlette.config import environ
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from httpx import AsyncClient, ASGITransport

environ["TESTING"] = "true"

from openanalytics.config import HOST, PORT, TEST_DATABASE_URL
from openanalytics.database import metadata, database
from openanalytics.main import app


@pytest.fixture(scope="session")
async def lifespan():
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture(scope="session", autouse=True)
async def create_test_database():
    url = str(TEST_DATABASE_URL)
    engine = create_engine(url)
    assert not database_exists(url), "Test database already exists. Aborting tests."
    create_database(url)
    metadata.create_all(engine)
    yield
    drop_database(url)


@pytest.fixture(scope="session")
async def http_client(lifespan):
    async with AsyncClient(transport=ASGITransport(app), base_url=f"http://{HOST}:{PORT}") as client:
        yield client
