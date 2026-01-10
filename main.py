from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, text
from datetime import datetime
import os
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Database (Render provides DATABASE_URL env var)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://qcruser:Quick@Sp-456782@localhost/qcrdb")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Tables
customers = Table("customers", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("email", String),
    Column("phone", String),
    Column("address", String),
    Column("notes", String),
    Column("created_at", DateTime, default=datetime.utcnow)
)

tickets = Table("tickets", metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_name", String),
    Column("customer_email", String),
    Column("customer_phone", String),
    Column("device_type", String),
    Column("brand", String),
    Column("model", String),
    Column("serial", String),
    Column("password", String),
    Column("faults", String),
    Column("other_fault", String),
    Column("accessories", String),
    Column("estimated_cost", Float),
    Column("created_at", DateTime, default=datetime.utcnow)
)

invoices = Table("invoices", metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_name", String),
    Column("amount", Float),
    Column("description", String),
    Column("created_at", DateTime, default=datetime.utcnow)
)

metadata.create_all(engine)

# Simple admin login (change password later)
ADMIN_USER = "admin"
ADMIN_PASS = "qcr2026"

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("booking.html", {"request": request})

@app.post("/book")
async def book(
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    customer_phone: str = Form(...),
    service_type: str = Form(...),
    appointment_date: str = Form(...),
    appointment_time: str = Form(...),
    description: str = Form("")
):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO bookings (customer_name, customer_email, customer_phone, service_type, appointment_date, appointment_time, description, created_at)
            VALUES (:name, :email, :phone, :service, :date, :time, :desc, NOW())
        """), {
            "name": customer_name,
            "email": customer_email,
            "phone": customer_phone,
            "service": service_type,
            "date": appointment_date,
            "time": appointment_time,
            "desc": description
        })
        conn.commit()

    return HTMLResponse(f"""
    <h1 style="color:green;text-align:center;margin-top:100px">Appointment Booked!</h1>
    <h2 style="text-align:center">Thank you {customer_name}</h2>
    <p style="text-align:center;font-size:24px">
      Service: {service_type}<br>
      Date: {appointment_date}<br>
      Time: {appointment_time}<br>
      We will contact you on {customer_phone}
    </p>
    <p style="text-align:center;margin-top:50px">
      <a href="/">← Book Another</a> | <a href="/admin">Admin Dashboard</a>
    </p>
    """)

@app.get("/login")
async def login_page(request: Request):
    return HTMLResponse("""
    <div style="max-width:400px;margin:auto;padding:50px;text-align:center">
      <h1 style="color:#00C4B4">Admin Login</h1>
      <form action="/login" method="post">
        <input name="username" placeholder="Username" style="width:100%;padding:14px;margin:10px 0;border-radius:8px" required>
        <input name="password" type="password" placeholder="Password" style="width:100%;padding:14px;margin:10px 0;border-radius:8px" required>
        <button type="submit" style="background:#00C4B4;color:white;padding:15px;width:100%;border:none;border-radius:8px;cursor:pointer">Login</button>
      </form>
    </div>
    """)

@app.post("/login")
async def do_login(username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USER and password == ADMIN_PASS:
        return RedirectResponse("/admin", status_code=303)
    return HTMLResponse("<h2 style='color:red;text-align:center'>Wrong credentials</h2><p style='text-align:center'><a href='/login'>← Try again</a></p>")

@app.get("/admin")
async def admin(request: Request):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM bookings ORDER BY created_at DESC"))
        bookings = result.fetchall()
    rows = ""
    for b in bookings:
        rows += f"<tr><td>{b[0]}</td><td>{b[1]}</td><td>{b[2]}</td><td>{b[3]}</td><td>{b[4]}</td><td>{b[5]}</td><td>{b[6]}</td><td>{b[7] or ''}</td><td>{b[8]}</td></tr>"
    return HTMLResponse(f"""
    <style>
      body {{font-family:'Segoe UI',sans-serif;background:#f8f9fa;margin:0;padding:20px}}
      .header {{background:#000;color:white;padding:20px;text-align:center;border-radius:12px}}
      .content {{max-width:1200px;margin:auto}}
      table {{width:100%;border-collapse:collapse;margin-top:30px;background:white;box-shadow:0 4px 10px rgba(0,0,0,0.1)}}
      th {{background:#00C4B4;color:white;padding:15px}}
      td {{padding:15px;border-bottom:1px solid #eee}}
      tr:hover {{background:#f0f8ff}}
    </style>
    <div class="header">
      <h1>QCR Admin Dashboard</h1>
    </div>
    <div class="content">
      <h2>All Bookings ({len(bookings)})</h2>
      <table>
        <tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Service</th><th>Date</th><th>Time</th><th>Description</th><th>Booked At</th></tr>
        {rows if rows else "<tr><td colspan='9' style='text-align:center'>No bookings yet</td></tr>"}
      </table>
      <p style="text-align:center;margin-top:50px"><a href="/login" style="color:#00C4B4">Logout</a></p>
    </div>
    """)
