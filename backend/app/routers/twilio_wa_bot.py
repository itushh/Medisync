from fastapi import APIRouter, Form, HTTPException, status
from app.lib.twilio_client import client as twilio_client
from app.lib.gemini_client import generate
from app.lib.logger import logger
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

TWILIO_TEMP_NUMBER = os.getenv("TWILIO_TEMP_NUMBER")
if not TWILIO_TEMP_NUMBER:
    logger.error("TWILIO_TEMP_NUMBER not set in environment variables")


def send_whatsapp_message(to: str, body: str) -> None:
    """
    Helper to send a WhatsApp message via Twilio.
    Raises Exception if sending fails.
    """
    try:
        twilio_client.messages.create(
            body=body,
            from_=f"whatsapp:{TWILIO_TEMP_NUMBER}",
            to=to,
        )
        logger.info(f"Message sent to {to}")
    except Exception as e:
        logger.error(f"Twilio send error: {e}")
        raise


@router.post("/temp")
async def respond_temp(From: str = Form(...), Body: str = Form(...)):
    """
    Twilio webhook (temporary).
    Always replies with a maintenance message.
    """
    try:
        send_whatsapp_message(
            to=From,
            body="Sorry to bother you! Server under maintenance."
        )
        return {"status": "message sent"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {e}"
        )


@router.post("/respond")
async def respond(From: str = Form(...), Body: str = Form(...)):
    """
    Twilio webhook.
    Uses Gemini to generate a reply from the incoming message body.
    """
    gemini_response = generate(Body)

    if gemini_response.get("status") == "error":
        error_msg = "Sorry to bother you! Something went wrong"
        logger.warning(f"Gemini error for input '{Body}': {gemini_response}")
        try:
            send_whatsapp_message(to=From, body=error_msg)
            return {"status": "message sent"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to send error message: {e}"
            )

    try:
        send_whatsapp_message(to=From, body=gemini_response["output"])
        return {"status": "message sent"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send Gemini response: {e}"
        )
