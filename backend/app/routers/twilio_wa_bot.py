from fastapi import APIRouter, Form
from app.lib.twilio_client import client as twilio_client
import os
from dotenv import load_dotenv
from app.lib.gemini_client import generate

load_dotenv()

twilio_mob = os.getenv("TWILIO_TEMP_NUMBER")

router = APIRouter()


# 
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
            body="Sorry to bother you! Server under maintainance..",
            from_=f'whatsapp:{twilio_mob}',
            to=From 
        )
        return {"status": "message sent"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    
    
@router.post("/respond")
async def respond(From: str = Form(...), Body: str = Form(...)):
    """
    Twilio posts here when a WhatsApp message arrives.
    `From` = sender's number
    `Body` = message text
    """
    gemini_responce = generate(Body)
    if gemini_responce["status"] == "error":
        try:
            twilio_client.messages.create(
                # body=f"You said: {Body}.",
                body="Sorry to bother you! Something went wrong",
                from_=f'whatsapp:{twilio_mob}',
                to=From 
            )
            return {"status": "message sent"}
        except Exception as e:
            return {"status": "error", "detail": str(e)}
    else:
        try:
            twilio_client.messages.create(
                # body=f"You said: {Body}.",
                body= gemini_responce["output"],
                from_= f'whatsapp:{twilio_mob}',
                to= From 
            )
            return {"status": "message sent"}
        except Exception as e:
            return {"status": "error", "detail": str(e)}