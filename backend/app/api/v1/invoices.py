from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_invoices():
    return {"status": "ok", "module": "invoices"}
