from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
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

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mount static files (for PDF downloads)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database (Render provides DATABASE_URL env var)
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

metadata.create_all(engine)

# Simple admin login (change this later)
ADMIN_USER = "alan"
ADMIN_PASS = "qcr123"

# Gmail credentials (use app password for security)
GMAIL_USER = "yourgmail@gmail.com"
GMAIL_PASS = "your-app-password"  # Create app password in Google account settings

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

@app.get("/calendar")
async def calendar():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT appointment_date, COUNT(*) FROM bookings GROUP BY appointment_date"))
        dates = result.fetchall()
    calendar_html = "<h2 style='text-align:center;color:#00C4B4'>Appointment Calendar</h2><table style='margin:auto;width:80%;border-collapse:collapse'>"
    calendar_html += "<tr><th>Date</th><th>Bookings</th></tr>"
    for date, count in dates:
        calendar_html += f"<tr><td>{date}</td><td>{count}</td></tr>"
    calendar_html += "</table><p style='text-align:center'><a href='/admin'>← Back to Dashboard</a></p>"
    return HTMLResponse(calendar_html)

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

    # Auto email confirmation (Gmail backup)
    try:
        msg = MIMEText(f"Hi {customer_name}!\nYour appointment is booked!\nService: {service_type}\nDate: {appointment_date}\nTime: {appointment_time}\nThank you!")
        msg['Subject'] = "Appointment Confirmation - Quick Click Repairs"
        msg['From'] = GMAIL_USER
        msg['To'] = customer_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        print("Email error:", str(e))

    # PDF ticket generation
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Quick Click Repairs - Ticket")
    c.drawString(100, 730, f"Customer: {customer_name}")
    c.drawString(100, 710, f"Service: {service_type}")
    c.drawString(100, 690, f"Date: {appointment_date}")
    c.drawString(100, 670, f"Time: {appointment_time}")
    c.drawString(100, 650, f"Phone: {customer_phone}")
    c.drawString(100, 630, f"Total Estimated Cost: £{estimated_cost:.2f}" if 'estimated_cost' in locals() else "TBD")
    c.save()
    buffer.seek(0)

    return FileResponse(buffer, media_type="application/pdf", filename="ticket.pdf")
