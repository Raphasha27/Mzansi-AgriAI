from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, FileResponse
from src.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


class TrialHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Powered-By"] = "Kirov Dynamics"
        response.headers["X-Trial"] = "true"
        return response


BASE = Path(__file__).resolve().parent
STATIC = BASE / "static"

app = FastAPI(
    title="Mzansi AgriAI",
    description="AI advisory for small-scale South African farmers",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrialHeadersMiddleware)


@app.get("/")
async def index():
    return FileResponse(str(STATIC / "index.html"))


app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")
app.include_router(router, prefix="/api/v1")
