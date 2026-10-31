from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_plans():
    return {"status": "ok", "module": "plans"}
