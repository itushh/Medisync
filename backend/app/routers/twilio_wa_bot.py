from fastapi import APIRouter, Form
from app.lib.twilio_client import client as twilio_client
import os
from dotenv import load_dotenv

load_dotenv()

twilio_mob = os.getenv("TWILIO_TEMP_NUMBER")

router = APIRouter(prefix="/twilio/whatsapp", tags=["whatsapp"])

@router.post("/respond")
def respond():
    return {"message": "Under construction"}

@router.post("/temp")
async def respond_temp(From: str = Form(...), Body: str = Form(...)):
    """
    Twilio posts here when a WhatsApp message arrives.
    `From` = sender's number
    `Body` = message text
    """
    try:
        twilio_client.messages.create(
            # body=f"You said: {Body}.",
            body="Hey! please integrate gemini first.",
            from_=f'whatsapp:{twilio_mob}',
            to=From 
        )
        return {"status": "message sent"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}