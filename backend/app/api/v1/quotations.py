from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_quotations():
    return {"status": "ok", "module": "quotations"}
