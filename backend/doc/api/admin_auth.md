# 🔐 Admin Authentication API

## Login

Authenticate an admin and receive an access token (stored as an HTTP-only cookie).

### Request

**Endpoint:**

```
POST /admin/login
```

**Body (JSON):**

```json
{
  "email": "admin@example.com",
  "key": "your-admin-key"
}
```

### Response

**Success (200):**

```json
{
  "access_token": "<JWT_TOKEN>",
  "message": "Logged in successfully"
}
```

* The `access_token` is also set as a secure **HTTP-only cookie** named `access_token`.
* The cookie will automatically be sent with subsequent requests (no need to manually attach the token from frontend).
* Token expiry: **1 month**

**Failure (401):**

```json
{
  "detail": "Invalid credentials"
}
```

**Failure (500):**

```json
{
  "detail": "Internal server error"
}
```

## Logout

Log out the current admin. The server will remove the authentication cookie.

### Request

**Endpoint:**

```
POST /admin/logout
```

**Headers:**
Must include the `access_token` cookie (sent automatically if logged in).

**Body:**
*No body required.*

### Response

**Success (200):**

```json
{
  "message": "Logged out successfully"
}
```

**Failure (401):**

```json
{
  "detail": "Invalid credentials"
}
```

**Failure (500):**

```json
{
  "detail": "Internal server error"
}
```

---

## Notes for Frontend Developers

* **Cookies are HTTP-only** → you cannot access `access_token` from JavaScript. This protects against XSS.
* Ensure your frontend uses `fetch` or `axios` with `{ credentials: "include" }` so cookies are sent with requests.

  ```js
  fetch("/api/protected-route", {
    method: "GET",
    credentials: "include" // ⬅ important
  });
  ```
* Use `/login` to authenticate and `/logout` to clear the session.
* After login, you don’t need to manually store the token—just rely on cookies.

---

Thank You!
