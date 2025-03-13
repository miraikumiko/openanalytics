import contextlib
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from openanalytics.config import HOST, PORT
from openanalytics.database import run_migrations
from openanalytics.routes.api import api_routes
from openanalytics.utils.auth import AuthBackend
from openanalytics.utils.scheduler import scheduler_start

routes = [
    Mount("/api", routes=api_routes)
]

middleware = [
    Middleware(
        AuthenticationMiddleware,
        backend=AuthBackend()
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
    await scheduler_start()
    await run_migrations()
    yield


app = Starlette(routes=routes, middleware=middleware, lifespan=lifespan)


def main():
    uvicorn.run(app, host=HOST, port=PORT)
