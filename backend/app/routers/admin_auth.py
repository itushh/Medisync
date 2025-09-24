from fastapi import APIRouter, HTTPException, Response, status
from app.models.admin import AdminLogin, Token
from app.lib.supabase_client import supabase
from app.auth.jwt_handler import create_access_token
from app.lib.logger import logger
from datetime import timedelta

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 60*12*30 #1 month


@router.post("/login", response_model=Token)
def login(admin: AdminLogin, response: Response):
    try:
        res = (
            supabase.table("users")
            .select("name, email, key")
            .eq("email", admin.email)
            .execute()
        )
    except Exception as e:
        logger.error(f"Supabase error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    if not res.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    user = res.data[0]

    if user["key"] != admin.key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token_data = {"sub": admin.email}
    access_token = create_access_token(
        token_data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,        # must be True in production with HTTPS
        samesite="lax",      # safer against CSRF
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return {"access_token": access_token, "message": "Logged in successfully"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
    )
    return {"message": "Logged out successfully"}
