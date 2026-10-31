from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_products():
    return {"status": "ok", "module": "products"}
