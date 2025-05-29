from fastapi import APIRouter, Response


default_router = APIRouter()


@default_router.get("/")
async def root() -> Response:
    return Response(content="Scheduler API is running.", media_type="text/plain")


@default_router.get("/ping")
async def ping() -> Response:
    return Response(content="pong", media_type="text/plain")


@default_router.get("/healthcheck")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@default_router.get("/ready")
async def ready() -> dict[str, str]:
    return {"status": "ready"}
