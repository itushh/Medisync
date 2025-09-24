Perfect, I’ll mirror the clean style of your **Auth API docs** and prepare a standalone `.md` for your Twilio WhatsApp routes.

---

# 💬 WhatsApp Bot API – Twilio Integration

This document explains how the `/temp` and `/respond` routes work with Twilio’s WhatsApp webhook.
These routes are automatically called by Twilio when a WhatsApp message is received.

---

## **POST /temp**

Temporary endpoint. Always replies with a **maintenance message** regardless of the input.

### Request (from Twilio)

**Endpoint:**

```
POST /temp
```

**Body (x-www-form-urlencoded):**

```
From=whatsapp:+1234567890
Body=Hello
```

* `From`: The sender’s WhatsApp number (prefixed with `whatsapp:`).
* `Body`: The text message sent by the user.

### Response

**Success (200):**

```json
{
  "status": "message sent"
}
```

**Failure (500):**

```json
{
  "detail": "Failed to send message: <error details>"
}
```

### Behavior

* The user always receives:

  ```
  Sorry to bother you! Server under maintenance.
  ```

---

## **POST /respond**

Main bot endpoint. Uses **Gemini** to generate a reply based on the user’s message.

### Request (from Twilio)

**Endpoint:**

```
POST /respond
```

**Body (x-www-form-urlencoded):**

```
From=whatsapp:+1234567890
Body=Tell me a joke
```

* `From`: The sender’s WhatsApp number (prefixed with `whatsapp:`).
* `Body`: The incoming message text.

### Response

**Success (200):**

```json
{
  "status": "message sent"
}
```

**Failure (500):**

```json
{
  "detail": "Failed to send Gemini response: <error details>"
}
```

### Behavior

1. The message body (`Body`) is passed to **Gemini**.
2. If Gemini succeeds → reply is sent back to the user.
3. If Gemini fails → user receives a fallback error message:

   ```
   Sorry to bother you! Something went wrong
   ```

---

## ⚠️ Notes for Frontend Developers

* You normally **don’t call these routes directly** — Twilio does it automatically when a user sends a WhatsApp message.
* To test manually, you can `POST` form-encoded data (like Twilio does):

```bash
curl -X POST http://localhost:8000/respond \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Hello bot"
```

* All outgoing messages come **from the configured Twilio WhatsApp number**.
* If `TWILIO_TEMP_NUMBER` is not set in `.env`, message sending will fail.

---

“Is a reply still a reply if it’s only sent by an algorithm and never truly meant?”

---

Do you want me to also add a **sequence diagram** (in Mermaid) showing how **WhatsApp → Twilio → FastAPI → Gemini → Twilio → WhatsApp** works? That might help frontend/backend devs visualize the flow.
