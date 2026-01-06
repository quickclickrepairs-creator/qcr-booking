from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, text
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Render provides DATABASE_URL environment variable
import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://qcruser:Quick@Sp-456782@localhost/qcrdb")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

bookings = Table(
    "bookings", metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_name", String),
    Column("customer_email", String),
    Column("customer_phone", String),
    Column("service_type", String),
    Column("appointment_date", String),
    Column("appointment_time", String),
    Column("description", String),
    Column("created_at", DateTime, default=datetime.utcnow)
)

metadata.create_all(engine)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("booking.html", {"request": request})

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

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
      <a href="/">← Book Another</a>
    </p>
    """)
@app.get("/admin")
async def admin(request: Request):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM bookings ORDER BY created_at DESC"))
        bookings = result.fetchall()
    rows = ""
    for b in bookings:
        rows += f"<tr><td>{b.id}</td><td>{b.customer_name}</td><td>{b.customer_email}</td><td>{b.customer_phone}</td><td>{b.service_type}</td><td>{b.appointment_date}</td><td>{b.appointment_time}</td><td>{b.description or ''}</td><td>{b.created_at}</td></tr>"
    return HTMLResponse(f"""
    <h1 style="text-align:center;color:#00C4B4">QCR Admin Dashboard</h1>
    <h2 style="text-align:center">All Bookings ({len(bookings)})</h2>
    <table style="margin:auto;width:90%;border-collapse:collapse">
      <tr style="background:#00C4B4;color:white">
        <th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Service</th><th>Date</th><th>Time</th><th>Description</th><th>Booked At</th>
      </tr>
      {rows or "<tr><td colspan='9'>No bookings yet</td></tr>"}
    </table>
    <p style="text-align:center;margin-top:50px"><a href="/">← Back to Booking</a></p>
    """)
