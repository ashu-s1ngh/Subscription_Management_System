from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_payments():
    return {"status": "ok", "module": "payments"}
