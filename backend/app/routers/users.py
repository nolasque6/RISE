from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import UserResponse, UserUpdate, UserLogin, UserRegister, TokenResponse
from app.services.authentication_service import (hash_password, verify_password, create_token, get_current_user)

fake_users_db = {}

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister):
    if user_data.email in fake_users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered")

    user_id = len(fake_users_db) + 1
    hashed_password = hash_password(user_data.password)

    fake_users_db[user_data.email] = {
        "id": user_id,
        "full_name": user_data.full_name,
        "email": user_data.email,
        "hashed_password": hashed_password
    }
    return {"message": "User registered successfully", "user_id": user_id}

@router.post("/login", response_model=TokenResponse)
async def login_user(credentials: UserLogin):
    user = fake_users_db.get(credentials.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    password_is_correct = verify_password(credentials.password, user["hashed_password"])
    if not password_is_correct:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_token(user_id=str(user["id"]))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user_id: str = Depends(get_current_user)):
    for user in fake_users_db.values():
        if str(user["id"]) == current_user_id:
            return {
                "id": user["id"],
                "full_name": user["full_name"],
                "email": user["email"]
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/me", response_model=UserResponse)
async def update_my_profile(user_update: UserUpdate, current_user_id: str = Depends(get_current_user)):
    for old_email, user in list(fake_users_db.items()):
        if str(user["id"]) == current_user_id:
            if (user_update.email and user_update.email != user["email"] and user_update.email in fake_users_db):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use by another account")
            
            user["full_name"] = user_update.full_name
            user["email"] = user_update.email

            if user_update.email != old_email:
                fake_users_db[user_update.email] = fake_users_db.pop(old_email)
            return {
                "id": user["id"],
                "full_name": user["full_name"],
                "email": user["email"]
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")