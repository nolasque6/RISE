from fastapi import APIRouter
from app.schemas.user import UserResponse, UserUpdate


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}", response_model=UserResponse)
async def get_current_user(user_id: int):
    return {
        "id": user_id,
        "full_name": "jean nono",
        "email": "jean.nono@example.com"
    }

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate):
    return {
        "id": user_id,
        "full_name": user_update.full_name,
        "email": user_update.email
    }