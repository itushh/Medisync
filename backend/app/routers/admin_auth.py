from fastapi import APIRouter, HTTPException, Response
from app.models.admin import AdminLogin, Token
from app.lib.supabase_client import supabase
from app.auth.jwt_handler import create_access_token

router = APIRouter()

@router.post("/login", response_model=Token)
def login(admin: AdminLogin, response: Response):
    res = supabase.table("users").select("name, email, key").eq("email", admin.email).execute()
    
    if not res.data or res.data[0]["key"] != admin.key:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": admin.email})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,      # True in production with HTTPS
        samesite="lax",    # or "strict" based on your needs
        max_age=30*12*3600       # 1 month
    )
    return {"message": "Logged in successfully"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",   # should match the path used when setting the cookie
    )
    return {"message": "Logged out successfully"}