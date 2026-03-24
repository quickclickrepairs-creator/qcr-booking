import os
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request, Form, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

# ========================= CONFIG =========================
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required")

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-to-a-long-random-string-in-production")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_FROM = os.getenv("YOUR_WHATSAPP_NUMBER", "whatsapp:+447863743275")

print(f"[INFO] Starting Quick Click Repairs | DB URL starts with: {DATABASE_URL[:60]}...")

# ========================= DATABASE =========================
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # Critical for Render stability
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ========================= MODELS =========================
class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    business_name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    check_in_at = Column(DateTime, nullable=True)

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    customer_email = Column(String, nullable=True)
    device_type = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    fault_type = Column(String, nullable=False)
    faults = Column(Text, nullable=False)
    accessories = Column(String, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    status = Column(String, default="Open")
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables safely
try:
    Base.metadata.create_all(bind=engine)
    print("[INFO] Database tables created or already exist")
except Exception as e:
    print(f"[ERROR] Table creation failed: {e}")

# ========================= APP =========================
app = FastAPI(title="Quick Click Repairs")

serializer = URLSafeTimedSerializer(SECRET_KEY)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# WhatsApp helper
def send_whatsapp(to_phone: str, message: str):
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        print("[WARNING] Twilio not configured")
        return False
    try:
        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        if not to_phone.startswith("whatsapp:"):
            to_phone = f"whatsapp:{to_phone}"
        msg = client.messages.create(from_=WHATSAPP_FROM, body=message, to=to_phone)
        print(f"[INFO] WhatsApp sent: {msg.sid}")
        return True
    except Exception as e:
        print(f"[ERROR] WhatsApp failed: {e}")
        return False

# Auth helpers
def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None
    try:
        return serializer.loads(session_id, max_age=86400)
    except (BadSignature, SignatureExpired):
        return None

def require_auth(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401)
    return user

# HTML Layout (same nice dark theme)
def get_page_layout(title: str, content: str, active: str = ""):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title} - Quick Click Repairs</title>
        <style>
            *{{margin:0;padding:0;box-sizing:border-box}}
            body{{font-family:Arial,sans-serif;background:#1a1a1a;color:#fff}}
            .header{{background:#222;padding:15px 30px;display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid #00C4B4}}
            .logo{{font-size:22px;font-weight:bold;color:#00C4B4}}
            .sidebar{{width:240px;background:#222;padding:20px 0;border-right:1px solid #333}}
            .sidebar a{{display:block;padding:14px 25px;color:#ccc;text-decoration:none}}
            .sidebar a:hover,.sidebar a.active{{background:#00C4B4;color:#000;font-weight:bold}}
            .main-content{{flex:1;padding:30px}}
            .btn{{background:#00C4B4;color:#000;padding:10px 20px;border:none;border-radius:5px;font-weight:bold;cursor:pointer;text-decoration:none}}
            table{{width:100%;border-collapse:collapse;background:#222}}
            th{{background:#333;padding:14px;text-align:left;color:#00C4B4}}
            td{{padding:14px;border-bottom:1px solid #333}}
        </style>
    </head>
    <body>
        <div class="header"><div class="logo">Quick Click Repairs</div></div>
        <div style="display:flex;min-height:calc(100vh - 63px)">
            <div class="sidebar">
                <a href="/admin/dashboard" class="{'active' if active=='dashboard' else ''}">Dashboard</a>
                <a href="/admin/customers" class="{'active' if active=='customers' else ''}">Customers</a>
                <a href="/admin/tickets" class="{'active' if active=='tickets' else ''}">Tickets</a>
                <a href="/logout">Logout</a>
            </div>
            <div class="main-content">
                {content}
            </div>
        </div>
    </body>
    </html>
    """

# Basic routes (expand later)
@app.get("/", response_class=HTMLResponse)
async def home():
    return """<h1 style="text-align:center;margin-top:100px;color:#00C4B4">Quick Click Repairs<br><small>Bookings only in-store • Call 023 8036 1277</small></h1>"""

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def dashboard(user = Depends(require_auth)):
    content = "<h1>Welcome to Dashboard</h1><p>Everything is working! Add customers and tickets below.</p>"
    return HTMLResponse(get_page_layout("Dashboard", content, "dashboard"))

# Add more routes (customers, tickets, login, etc.) as needed

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
