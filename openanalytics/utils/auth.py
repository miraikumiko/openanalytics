from argon2 import PasswordHasher
from starlette.authentication import AuthenticationBackend, AuthCredentials
from starlette.requests import Request
from openanalytics.database import database
from openanalytics.models import User, Site

ph = PasswordHasher()


class CustomAuthBackend(AuthenticationBackend):
    def __init__(self, backend1, backend2):
        self.backend1 = backend1
        self.backend2 = backend2

    async def authenticate(self, conn: Request):
        user = await self.backend1.authenticate(conn)

        if user:
            return user

        return await self.backend2.authenticate(conn)


class BearerAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: Request):
        token = conn.headers.get("Authorization")

        if token:
            user = await database.fetch_one(User.select().where(User.c.token == token))

            if user:
                return AuthCredentials(["authenticated"]), user


class SiteTokenBackend(AuthenticationBackend):
    async def authenticate(self, conn: Request):
        token = conn.headers.get("Token")

        if token:
            site = await database.fetch_one(Site.select().where(Site.c.token == token))

            if site:
                conn.state.site = site
                return AuthCredentials(["site_token"]), site
