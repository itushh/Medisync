import os
from app.lib.logger import logger
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import admin_auth, twilio_wa_bot
from app.auth.dependencies import get_current_user
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Medisync Server")

""" CORS configuration
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) """

""" Trusted hosts
trusted_hosts = os.getenv("TRUSTED_HOSTS", "*").split(",")
app.add_middleware(TrustedHostMiddleware, allowed_hosts=trusted_hosts) """

# routers
app.include_router(admin_auth.router, prefix="/admin", tags=["Admin"])
app.include_router(twilio_wa_bot.router, prefix="/twilio", tags=["Twilio WA Bot"])

# health check
@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "Server is live!"}

""" protected route example
@app.get("/protected", tags=["Protected"])
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['sub']}, you are authorized!"} """

# global error handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP error occurred: {exc.status_code} {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Server is starting...")

# shutdown even
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Server is shutting down...")
