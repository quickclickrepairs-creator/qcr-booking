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

# Database (use Render env var for production)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://qcruser:Quick@Sp-456782@localhost/qcrdb")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Tables
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

# Login (change in production!)
ADMIN_USER = "alan"
ADMIN_PASS = "qcr123"

# Secrets (use Render env vars!)
GMAIL_USER = os.getenv("GMAIL_USER", "your.email@gmail.com")
GMAIL_PASS = os.getenv("GMAIL_PASS", "your-app-password")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
YOUR_WHATSAPP = "whatsapp:+447863743275"

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
    booking_rows = ''.join(f"<tr><td>{x.id}</td><td>{x.customer_name}</td><td>{x.customer_email}</td><td>{x.customer_phone}</td><td>{x.service_type}</td><td>{x.appointment_date}</td><td>{x.appointment_time}</td><td>{x.description or ''}</td><td>{x.created_at}</td></tr>" for x in b) or "<tr><td colspan='9'>No bookings</td></tr>"
    ticket_rows = ''.join(f"<tr><td>{x.id}</td><td>{x.customer_name}</td><td>{x.device_type}</td><td>{x.brand} {x.model}</td><td>£{x.estimated_cost:.2f}</td><td>{x.created_at}</td></tr>" for x in t) or "<tr><td colspan='6'>No tickets</td></tr>"
    customer_rows = ''.join(f"<tr><td>{x.id}</td><td>{x.name}</td><td>{x.email}</td><td>{x.phone}</td><td>{x.created_at}</td></tr>" for x in c) or "<tr><td colspan='5'>No customers</td></tr>"
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Quick Click Repairs – Dashboard</title>
      <style>
        * {margin:0;padding:0;box-sizing:border-box}
        body {font-family: 'Segoe UI', Arial, sans-serif; background:#1e1e1e; color:#e0e0e0; margin:0}
        header {background:#000; padding:15px 30px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 4px 10px rgba(0,0,0,0.5)}
        header h1 {color:#fff; font-size:24px}
        .search {background:#333; border-radius:20px; padding:8px 15px; color:white; border:none; width:300px}
        .user {display:flex; align-items:center; gap:10px}
        .user img {width:40px; height:40px; border-radius:50%}
        nav {background:#2a2a2a; padding:20px; min-width:200px}
        nav ul {list-style:none}
        nav li {margin:10px 0}
        nav a {color:#aaa; text-decoration:none; font-size:16px; display:block; padding:10px; border-radius:8px}
        nav a:hover {background:#00C4B4; color:white}
        .main {display:flex}
        .content {flex:1; padding:30px}
        .welcome {font-size:36px; margin-bottom:40px}
        .get-started {display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:20px; margin-bottom:40px}
        .btn {background:#00C4B4; color:white; padding:30px; border-radius:12px; text-decoration:none; font-size:20px; font-weight:bold; text-align:center; display:flex; align-items:center; justify-content:center; gap:15px}
        .btn:hover {background:#00a89a}
        .icon {font-size:32px}
        .reminders {background:#2a2a2a; padding:25px; border-radius:12px}
        .reminders h2 {margin-bottom:20px}
        table {width:100%; border-collapse:collapse}
        th {background:#00C4B4; color:white; padding:12px; text-align:left}
        td {padding:12px; border-bottom:1px solid #444}
      </style>
    </head>
    <body>
      <header>
        <h1>Quick Click Repairs</h1>
        <input type="text" placeholder="Search all the things" class="search">
        <div class="user">
          <span>Alan ▼</span>
          <img src="https://i.imgur.com/placeholder-user.jpg" alt="User">
        </div>
      </header>
      <div class="main">
        <nav>
          <ul>
            <li><a href="/organizations">Organizations</a></li>
            <li><a href="/invoices">Invoices</a></li>
            <li><a href="/customer-purchases">Customer Purchases</a></li>
            <li><a href="/refurbs">Refurbs</a></li>
            <li><a href="/tickets">Tickets</a></li>
            <li><a href="/parts">Parts</a></li>
            <li><a href="/more">More</a></li>
          </ul>
        </nav>
        <div class="content">
          <div class="welcome">Welcome!</div>
          <div class="get-started">
            <a href="/new-customer" class="btn"><span class="icon">👤</span> + New Customer</a>
            <a href="/new-ticket" class="btn"><span class="icon">✔</span> + New Ticket</a>
            <a href="/new-checkin" class="btn"><span class="icon">📱</span> + New Check In</a>
            <a href="/new-invoice" class="btn"><span class="icon">🛒</span> + New Invoice</a>
            <a href="/new-estimate" class="btn"><span class="icon">📄</span> + New Estimate</a>
          </div>
          <div class="reminders">
            <h2>REMINDERS</h2>
            <table>
              <tr><th>MESSAGE</th><th>TIME</th><th>TECH</th><th>CUSTOMER</th></tr>
              <tr><td>No reminders yet</td><td>-</td><td>-</td><td>-</td></tr>
            </table>
            <button style="margin-top:20px;padding:10px 20px;background:#00C4B4;color:white;border:none;border-radius:8px;cursor:pointer">View All</button>
          </div>
          <h2>All Bookings</h2>
          <table>
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Service</th><th>Date</th><th>Time</th><th>Description</th><th>Booked</th></tr>
            {booking_rows}
          </table>
          <h2>All Tickets</h2>
          <table>
            <tr><th>ID</th><th>Customer</th><th>Device</th><th>Est. Cost</th><th>Created</th></tr>
            {ticket_rows}
          </table>
          <h2>All Customers</h2>
          <table>
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Created</th></tr>
            {customer_rows}
          </table>
          <p style="text-align:center;margin-top:50px"><a href="/calendar" style="color:#00C4B4">Calendar</a> | <a href="/login" style="color:#00C4B4">Logout</a></p>
        </div>
      </div>
    </body>
    </html>
    """)

# ... (add the other routes from previous messages for new-customer, new-ticket, etc.)
