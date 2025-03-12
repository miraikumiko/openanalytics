from starlette.authentication import AuthenticationBackend, AuthCredentials
from starlette.requests import Request
from openanalytics.database import database
from openanalytics.models import Site


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: Request):
        token = conn.headers.get("Token")

        if token:
            site = await database.fetch_one(Site.select().where(Site.c.token == token))

            if site:
                conn.state.site = site
                return AuthCredentials(["authenticated"]), site