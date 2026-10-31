from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_customers():
    return {"status": "ok", "module": "customers"}
