from datetime import date
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

    client = await database.fetch_one(Client.select().where(Client.c.ip == ip))
    site_visitor = 0 if client else 1

    await database.execute(
        Client.insert().values(
            ip=ip,
            country=country,
            os=os,
            browser=browser,
            referrer=referrer,
            page_url=page_url,
            visited_at=date.today(),
            site_id=site.id
        )
    )

    await database.execute(
        Site.update().where(Site.c.id == site.id).values(
            visitors=site.visitors + site_visitor,
            views=site.views + 1
        )
    )

    page = await database.fetch_one(Page.select().where(Page.c.url == page_url))

    if page:
        client = await database.fetch_one(Client.select().where(Client.c.page_url == page_url))
        page_visitor = 0 if client else 1

        await database.execute(
            Page.update().where(Page.c.id == page.id).values(
                visitors=page.visitors + page_visitor,
                views=page.views + 1
            )
        )
    else:
        await database.execute(
            Page.insert().values(
                url=page_url,
                visitors=1,
                views=1,
                site_id=site.id
            )
        )

    return JSONResponse({"status": "ok"})


api_routes = [
    Route("/send", analytics, methods=["POST"])
]
