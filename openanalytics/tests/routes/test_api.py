import pytest
from httpx import AsyncClient
from openanalytics.database import database
from openanalytics.models import Site
from openanalytics.main import app

DOMAIN = "example.com"
TOKEN = "ABCD1234"


@pytest.mark.asyncio(loop_scope="session")
async def test_analytics(http_client: AsyncClient) -> None:
    url = app.url_path_for("analytics")
    data = {
        "referrer": "https://duckduckgo.com/",
        "user_agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
        "page_url": "/blog",
        "ip": "127.0.0.1",
        "country": "Spain"
    }
    headers = {
        "Token": TOKEN
    }

    await database.execute(
        Site.insert().values(
            domain=DOMAIN,
            token=TOKEN,
            visitors=0,
            views=0
        )
    )

    response = await http_client.post(url, json=data)

    assert response.status_code == 403

    response = await http_client.post(url, json=data, headers=headers)

    assert response.status_code == 200
