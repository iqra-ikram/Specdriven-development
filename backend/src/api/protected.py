from fastapi import APIRouter, Depends
from backend.src.core.auth_middleware import get_current_user
from backend.src.models.auth_models import User

router = APIRouter()

@router.get("/protected-data")
def read_protected_data(current_user: User = Depends(get_current_user)):
    return {
        "message": "This is protected data",
        "user_id": current_user.id,
        "email": current_user.email
    }
