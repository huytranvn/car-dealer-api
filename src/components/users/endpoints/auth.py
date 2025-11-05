from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from configs.database import get_db
from components.users.schemas import LoginRequest, LoginResponse
from utils.auth import authenticate_user, create_access_token

router = APIRouter(prefix="/v1")


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return a bearer token.
    """
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return LoginResponse(access_token=access_token, token_type="bearer")

