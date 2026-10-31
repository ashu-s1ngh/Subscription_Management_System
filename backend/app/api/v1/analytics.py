from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_analytics():
    return {"status": "ok", "module": "analytics"}
