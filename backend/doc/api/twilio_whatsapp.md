

# Twilio Webhook routes

## Temp webhook

Temporary endpoint. Always replies with a **maintenance message** regardless of the input.

### Request (from Twilio)

**Endpoint:**

```
POST /twilio/whatsapp/temp
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

## Main webhook

Main bot endpoint. Uses **Gemini** to generate a reply based on the user’s message.

### Request (from Twilio)

**Endpoint:**

```
POST /twilio/whatsapp/respond
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

## Notes for Frontend Developers

* You normally **don’t call these routes directly** — Twilio does it automatically when a user sends a WhatsApp message.
* To test manually, you can `POST` form-encoded data (like Twilio does):

```bash
curl -X POST http://localhost:8000/twilio/whatsapp/respond \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Hello bot"
```

---
Thank You!