from json.decoder import JSONDecodeError
from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from user_agents import parse as ua_parse
from openanalytics.database import database
from openanalytics.models import Site, Page, Client


@requires("authenticated")
async def analytics(request: Request):
    site = getattr(request.state, "site", None)

    if not site:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)

    try:
        data = await request.json()
    except JSONDecodeError:
        return JSONResponse({"error": "Invalid or missing data"}, status_code=400)

    referrer = data.get("referrer")
    user_agent = data.get("user_agent")
    page_url = data.get("page_url")
    ip = data.get("ip")
    country = data.get("country")

    user_agent = ua_parse(user_agent)
    os = user_agent.os.family
    browser = user_agent.browser.family

    await database.execute(
        Client.insert().values(
            ip=ip,
            country=country,
            os=os,
            browser=browser,
            referrer=referrer,
            page_url=page_url,
            site_id=site.id
        )
    )

    client = await database.fetch_one(Client.select().where(Client.c.ip == ip))
    site_unique_visitor = 0 if client else 1

    await database.execute(
        Site.update().where(Site.c.id == site.id).values(
            unique_visitors=site.unique_visitors + site_unique_visitor,
            total_views=site.total_views + 1
        )
    )

    page = await database.fetch_one(Page.select().where(Page.c.url == page_url))

    if page:
        client = await database.fetch_one(Client.select().where(Client.c.page_url == page_url))
        page_unique_visitor = 0 if client else 1

        await database.execute(
            Page.update().where(Page.c.id == page.id).values(
                unique_visitors=page.unique_visitors + page_unique_visitor,
                total_views=page.total_views + 1
            )
        )
    else:
        await database.execute(
            Page.insert().values(
                url=page_url,
                unique_visitors=1,
                total_views=1,
                site_id=site.id
            )
        )

    return JSONResponse({"status": "ok"})


routes = [
    Route("/", analytics, methods=["POST"])
]
