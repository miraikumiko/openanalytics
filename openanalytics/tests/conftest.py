import pytest
from starlette.config import environ
from httpx import AsyncClient, ASGITransport

environ["TESTING"] = "true"

from openanalytics.config import HOST, PORT, DATABASE_TEST_URL
from openanalytics.database import database, run_migrations, drop_database
from openanalytics.main import app


@pytest.fixture(scope="session")
async def lifespan():
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture(scope="session", autouse=True)
async def create_test_database():
    await run_migrations(DATABASE_TEST_URL)
    yield
    await drop_database(DATABASE_TEST_URL)


@pytest.fixture(scope="session")
async def http_client(lifespan):
    async with AsyncClient(transport=ASGITransport(app), base_url=f"http://{HOST}:{PORT}") as client:
        yield client
