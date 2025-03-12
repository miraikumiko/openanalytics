from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


@requires("authenticated")
async def post(request: Request):
    site = getattr(request.state, "site", None)

    if not site:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)

    return JSONResponse({"status": "ok"})


routes = [
    Route("/", post, methods=["POST"])
]