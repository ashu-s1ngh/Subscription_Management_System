from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_staff():
    return {"status": "ok", "module": "staff"}
