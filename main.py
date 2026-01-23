from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, text
from datetime import datetime
import os

app = FastAPI()

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://qcruser:Quick@Sp-456782@localhost/qcrdb")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

customers = Table("customers", metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String),
    Column("last_name", String),
    Column("business_name", String),
    Column("email", String),
    Column("phone", String),
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

# Login credentials
ADMIN_USER = "alan"
ADMIN_PASS = "qcr123"

@app.get("/login")
async def login_page():
    return HTMLResponse("""
    <div style="max-width:400px;margin:100px auto;background:#2a2a2a;padding:40px;border-radius:15px;text-align:center">
      <h1 style="color:#00C4B4">Admin Login</h1>
      <form action="/login" method="post">
        <input name="username" placeholder="Username" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="password" type="password" placeholder="Password" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
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

    booking_rows = ''.join(f"<tr><td>{x.id}</td><td>{x.customer_name}</td><td>{x.customer_email}</td><td>{x.customer_phone}</td><td>{x.service_type}</td><td>{x.appointment_date}</td><td>{x.appointment_time}</td><td>{x.description or ''}</td><td>{x.created_at}</td></tr>" for x in b) or "<tr><td colspan='9'>No bookings</td></tr>"
    ticket_rows = ''.join(f"<tr><td>{x.id}</td><td>{x.customer_name}</td><td>{x.device_type}</td><td>£{x.estimated_cost:.2f}</td><td>{x.created_at}</td></tr>" for x in t) or "<tr><td colspan='5'>No tickets</td></tr>"
    customer_rows = ''.join(f"<tr><td>{x.id}</td><td>{x.first_name} {x.last_name}</td><td>{x.business_name or ''}</td><td>{x.email}</td><td>{x.phone}</td><td>{x.created_at}</td></tr>" for x in c) or "<tr><td colspan='6'>No customers</td></tr>"

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
        {booking_rows}
      </table>
      <h2>All Tickets ({len(t)})</h2>
      <table>
        <tr><th>ID</th><th>Customer</th><th>Device</th><th>Est. Cost</th><th>Created</th></tr>
        {ticket_rows}
      </table>
      <h2>All Customers ({len(c)})</h2>
      <table>
        <tr><th>ID</th><th>Name</th><th>Business</th><th>Email</th><th>Phone</th><th>Created</th></tr>
        {customer_rows}
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

    # Email confirmation
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

    # WhatsApp confirmation
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        message = client.messages.create(
            body=f"Hi {customer_name}! Your appointment is booked!\nService: {service_type}\nDate: {appointment_date}\nTime: {appointment_time}\nThank you for choosing Quick Click Repairs!",
            from_=YOUR_WHATSAPP,
            to=f"whatsapp:+44{customer_phone.lstrip('0')}"
        )
    except:
        pass

    # PDF ticket
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Quick Click Repairs - Ticket")
    c.drawString(100, 730, f"Customer: {customer_name}")
    c.drawString(100, 710, f"Service: {service_type}")
    c.drawString(100, 690, f"Date: {appointment_date}")
    c.drawString(100, 670, f"Time: {appointment_time}")
    c.drawString(100, 650, f"Phone: {customer_phone}")
    c.save()
    buffer.seek(0)

    return FileResponse(buffer, media_type="application/pdf", filename="ticket.pdf")
