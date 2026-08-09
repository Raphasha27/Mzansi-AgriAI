from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

STATIC = Path(__file__).resolve().parent / "static"


@router.get("/")
async def landing():
    return FileResponse(STATIC / "index.html")


@router.get("/api/health")
async def health():
    return {"status": "ok", "service": "Mzansi AgriAI", "powered_by": "Kirov Dynamics"}


@router.get("/api/advice")
async def advice():
    return {
        "crop": "maize",
        "season": "summer",
        "advice": "Plant after the first good soak. Apply split nitrogen dressing at knee height.",
        "confidence": 0.94,
    }