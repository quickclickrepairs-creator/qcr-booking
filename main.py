from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Optional
import secrets
import unittest

app = FastAPI(title="Sandbox-Safe API", version="1.0.0")

# In-memory stores (replace with real DB in production)
USERS: Dict[str, str] = {"admin": "password"}
SESSIONS: Dict[str, str] = {}  # token → username

# -----------------------------------------------------------------------------
# Models (JSON only)
# -----------------------------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class HealthResponse(BaseModel):
    status: str

class UserResponse(BaseModel):
    username: str

# -----------------------------------------------------------------------------
# Simple token auth (no jose/JWT – sandbox safe)
# -----------------------------------------------------------------------------
def create_token(username: str) -> str:
    token = secrets.token_urlsafe(32)
    SESSIONS[token] = username
    return token

def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.split(" ")[1]
    user = SESSIONS.get(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user

# -----------------------------------------------------------------------------
# Routes (JSON only)
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

@app.get("/me", response_model=UserResponse)
def me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}

# -----------------------------------------------------------------------------
# Tests (stdlib unittest only)
# -----------------------------------------------------------------------------
class APITests(unittest.TestCase):
    def test_health(self):
        self.assertEqual(health(), {"status": "ok"})

    def test_login_success(self):
        payload = LoginRequest(username="admin", password="password")
        resp = login(payload)
        self.assertIn("access_token", resp)
        self.assertIsInstance(resp["access_token"], str)

    def test_login_failure(self):
        with self.assertRaises(HTTPException) as cm:
            login(LoginRequest(username="admin", password="wrong"))
        self.assertEqual(cm.exception.status_code, 401)

    def test_token_flow(self):
        payload = LoginRequest(username="admin", password="password")
        login_resp = login(payload)
        token = login_resp["access_token"]
        
        # Simulate Depends by calling directly
        user = get_current_user(f"Bearer {token}")
        self.assertEqual(user, "admin")

        # Invalid token
        with self.assertRaises(HTTPException) as cm:
            get_current_user("Bearer wrongtoken")
        self.assertEqual(cm.exception.status_code, 401)

if __name__ == "__main__":
    unittest.main()
