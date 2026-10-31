from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_subscriptions():
    return {"status": "ok", "module": "subscriptions"}
