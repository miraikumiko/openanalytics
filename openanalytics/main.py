import contextlib
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from openanalytics.config import HOST, PORT, DATABASE_URL
from openanalytics.database import database, run_migrations
from openanalytics.routes.api import api_routes
from openanalytics.utils.auth import CustomAuthBackend, BearerAuthBackend, SiteTokenBackend


routes = [
    Mount("/api", routes=api_routes)
]

middleware = [
    Middleware(
        AuthenticationMiddleware,
        backend=CustomAuthBackend(
            backend1=BearerAuthBackend(),
            backend2=SiteTokenBackend()
        )
    ),
    Middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"]
    )
]


@contextlib.asynccontextmanager
async def lifespan(_):
    await run_migrations(DATABASE_URL)
    await database.connect()
    yield
    await database.disconnect()


app = Starlette(routes=routes, middleware=middleware, lifespan=lifespan)


def main():
    uvicorn.run(app, host=HOST, port=PORT)
