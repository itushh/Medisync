from fastapi import FastAPI, Depends
from app.routers import admin_auth
from app.routers import twilio_wa_bot
from app.auth.dependencies import get_current_user

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server if fucking live!"}

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['sub']}, you are authorized!"}

app.include_router(admin_auth.router)
app.include_router(twilio_wa_bot.router)
