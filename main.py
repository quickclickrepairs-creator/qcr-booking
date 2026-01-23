# Production‑Ready Starter Backend (Sandbox‑Safe)

"""
This version removes dependencies that are NOT available in the sandboxed
Python environment:
- ssl (indirectly via anyio networking features)
- python-jose (JWT)
- jinja2 (templates)
- python-multipart (form uploads)

Key changes:
- Uses JSON-only request bodies (no Form(), no file uploads)
- No template rendering (API-only JSON responses)
- Authentication is a SIMPLE, explicit token stub using stdlib only
  (replace with real JWT in a proper environment)
- Includes basic tests using unittest (stdlib)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import secrets
import unittest

app = FastAPI(title="Sandbox‑Safe API", version="1.0.0")

# -----------------------------------------------------------------------------
# In‑memory stores (replace with DB in production)
# -----------------------------------------------------------------------------
USERS: Dict[str, str] = {"admin": "password"}
SESSIONS: Dict[str, str] = {}

# -----------------------------------------------------------------------------
# Models (JSON only — avoids python‑multipart)
# -----------------------------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class HealthResponse(BaseModel):
    status: str

# -----------------------------------------------------------------------------
# Auth helpers (NO jose / JWT — sandbox safe stub)
# -----------------------------------------------------------------------------

def create_token(username: str) -> str:
    token = secrets.token_urlsafe(32)
    SESSIONS[token] = username
    return token


def require_token(token: str) -> str:
    user = SESSIONS.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user

# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}


@app.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    if USERS.get(payload.username) != payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(payload.username)
    return {"access_token": token}


@app.get("/me")
def me(token: str):
    """Token is passed as a query parameter to avoid headers/JWT complexity."""
    user = require_token(token)
    return {"username": user}

# -----------------------------------------------------------------------------
# Tests (stdlib only)
# -----------------------------------------------------------------------------
class APITests(unittest.TestCase):
    def test_health(self):
        self.assertEqual(health(), {"status": "ok"})

    def test_login_success(self):
        payload = LoginRequest(username="admin", password="password")
        resp = login(payload)
        self.assertIn("access_token", resp)

    def test_login_failure(self):
        with self.assertRaises(HTTPException):
            login(LoginRequest(username="admin", password="wrong"))

    def test_token_flow(self):
        payload = LoginRequest(username="admin", password="password")
        resp = login(payload)
        token = resp["access_token"]
        self.assertEqual(me(token)["username"], "admin")


if __name__ == "__main__":
    unittest.main()
