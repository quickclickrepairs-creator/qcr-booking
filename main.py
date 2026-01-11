from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, text
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from twilio.rest import Client

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://qcruser:Quick@Sp-456782@localhost/qcrdb")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

bookings = Table("bookings", metadata,
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

tickets = Table("tickets", metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_name", String),
    Column("customer_email", String),
    Column("customer_phone", String),
    Column("device_type", String),
    Column("brand", String),
    Column("model", String),
    Column("serial", String),
    Column("faults", String),
    Column("other_fault", String),
    Column("accessories", String),
    Column("estimated_cost", Float),
    Column("created_at", DateTime, default=datetime.utcnow)
)

customers = Table("customers", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("email", String),
    Column("phone", String),
    Column("address", String),
    Column("notes", String),
    Column("created_at", DateTime, default=datetime.utcnow)
)

metadata.create_all(engine)

# Credentials (CHANGE THESE!)
ADMIN_USER = "alan"
ADMIN_PASS = "qcr123"

GMAIL_USER = "your.email@gmail.com"
GMAIL_PASS = "your-app-password"  # https://myaccount.google.com/apppasswords

TWILIO_SID = "your_twilio_sid"
TWILIO_TOKEN = "your_twilio_auth_token"
YOUR_WHATSAPP = "whatsapp:+44YOURNUMBER"  # Your own number

@app.get("/login")
async def login_page():
    return HTMLResponse("""
    <div style="max-width:400px;margin:100px auto;text-align:center">
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
async def admin():
    with engine.connect() as conn:
        b = conn.execute(text("SELECT * FROM bookings ORDER BY created_at DESC")).fetchall()
        t = conn.execute(text("SELECT * FROM tickets ORDER BY created_at DESC")).fetchall()
        c = conn.execute(text("SELECT * FROM customers ORDER BY created_at DESC")).fetchall()
    return HTMLResponse(f"""
    <style>
      body {{font-family:'Segoe UI',sans-serif;background:#1e1e1e;color:#e0e0e0;margin:0;padding:20px}}
      .header {{background:#000;color:white;padding:20px;text-align:center;border-radius:12px}}
      .content {{max-width:1200px;margin:auto}}
      table {{width:100%;border-collapse:collapse;margin-top:30px;background:#2a2a2a;box-shadow:0 4px 10px rgba(0,0,0,0.5)}}
      th {{background:#00C4B4;color:white;padding:15px}}
      td {{padding:15px;border-bottom:1px solid #444}}
      tr:hover {{background:#3a3a3a}}
    </style>
    <div class="header">
      <h1>QCR Admin Dashboard</h1>
    </div>
    <div class="content">
      <h2>All Bookings ({len(b)})</h2>
      <table>
        <tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Service</th><th>Date</th><th>Time</th><th>Description</th><th>Booked</th></tr>
        {''.join(f"<tr><td>{x.id}</td><td>{x.customer_name}</td><td>{x.customer_email}</td><td>{x.customer_phone}</td><td>{x.service_type}</td><td>{x.appointment_date}</td><td>{x.appointment_time}</td><td>{x.description or ''}</td><td>{x.created_at}</td></tr>" for x in b) or "<tr><td colspan='9'>No bookings</td></tr>"}
      </table>
      <h2>All Tickets ({len(t)})</h2>
      <table>
        <tr><th>ID</th><th>Customer</th><th>Device</th><th>Est. Cost</th><th>Created</th></tr>
        {''.join(f"<tr><td>{x.id}</td><td>{x.customer_name}</td><td>{x.device_type}</td><td>£{x.estimated_cost:.2f}</td><td>{x.created_at}</td></tr>" for x in t) or "<tr><td colspan='5'>No tickets</td></tr>"}
      </table>
      <h2>All Customers ({len(c)})</h2>
      <table>
        <tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Created</th></tr>
        {''.join(f"<tr><td>{x.id}</td><td>{x.name}</td><td>{x.email}</td><td>{x.phone}</td><td>{x.created_at}</td></tr>" for x in c) or "<tr><td colspan='5'>No customers</td></tr>"}
      </table>
      <p style="text-align:center;margin-top:50px"><a href="/calendar" style="color:#00C4B4">Calendar</a> | <a href="/login" style="color:#00C4B4">Logout</a></p>
    </div>
    """)

@app.get("/calendar")
async def calendar():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT appointment_date, COUNT(*) FROM bookings GROUP BY appointment_date"))
        dates = result.fetchall()
    return HTMLResponse(f"""
    <div style="background:#1e1e1e;color:#e0e0e0;padding:40px">
      <h1 style="text-align:center;color:#00C4B4">Appointment Calendar</h1>
      <table style="margin:auto;width:80%;border-collapse:collapse;background:#2a2a2a">
        <tr><th style="background:#00C4B4;color:white;padding:15px">Date</th><th style="background:#00C4B4;color:white;padding:15px">Bookings</th></tr>
        {''.join(f"<tr><td>{d[0]}</td><td>{d[1]}</td></tr>" for d in dates) or "<tr><td colspan='2'>No appointments</td></tr>"}
      </table>
      <p style="text-align:center;margin-top:50px"><a href="/admin" style="color:#00C4B4">← Back to Dashboard</a></p>
    </div>
    """)

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
        conn.execute(bookings.insert().values(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            service_type=service_type,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            description=description
        ))
        conn.commit()

    # Email
    try:
        msg = MIMEText(f"Hi {customer_name}!\nYour appointment is booked!\nService: {service_type}\nDate: {appointment_date}\nTime: {appointment_time}\nThank you!")
        msg['Subject'] = "Appointment Confirmation - Quick Click Repairs"
        msg['From'] = GMAIL_USER
        msg['To'] = customer_email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)
    except:
        pass

    # WhatsApp
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        client.messages.create(
            body=f"Hi {customer_name}! Your appointment is booked!\nService: {service_type}\nDate: {appointment_date}\nTime: {appointment_time}\nThank you!",
            from_=YOUR_WHATSAPP,
            to=f"whatsapp:+44{customer_phone.lstrip('0')}"
        )
    except:
        pass

    return HTMLResponse(f"""
    <h1 style="color:green;text-align:center;margin-top:100px">Appointment Booked!</h1>
    <h2 style="text-align:center">Thank you {customer_name}!</h2>
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
    # Confirmation page - success message
    return HTMLResponse(f"""
    <html>
    <head><title>Booked!</title></head>
    <body style="font-family:Arial;background:#f0f8ff;text-align:center;padding:50px">
      <h1 style="color:green">Appointment Booked!</h1>
      <h2>Thank you {customer_name}!</h2>
      <p style="font-size:24px">
        Service: <strong>{service_type}</strong><br>
        Date: <strong>{appointment_date}</strong><br>
        Time: <strong>{appointment_time}</strong><br>
        We will contact you on <strong>{customer_phone}</strong>
      </p>
      <p style="margin-top:50px">
        <a href="/" style="color:#00C4B4;font-size:20px">← Book Another Appointment</a>
      </p>
    </body>
    </html>
    """)
