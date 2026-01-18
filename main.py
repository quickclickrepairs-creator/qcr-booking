from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from sqlalchemy import create_engine, text
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from twilio.rest import Client

app = FastAPI()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://qcruser:Quick@Sp-456782@localhost/qcrdb")
engine = create_engine(DATABASE_URL)

# Create customers table
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            business_name VARCHAR(150),
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            check_in_at TIMESTAMP
        )
    """))
    conn.commit()

# Credentials (use Render env vars for security)
ADMIN_USER = "alan"
ADMIN_PASS = "qcr123"

GMAIL_USER = os.getenv("GMAIL_USER", "your.email@gmail.com")
GMAIL_PASS = os.getenv("GMAIL_PASS", "your-app-password")

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID", "your-twilio-sid")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your-twilio-token")
YOUR_WHATSAPP = "whatsapp:+447863743275"

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
        result = conn.execute(text("SELECT * FROM customers ORDER BY created_at DESC"))
        customers = result.fetchall()

    rows = ""
    for c in customers:
        check_in = c.check_in_at.strftime("%Y-%m-%d %H:%M") if c.check_in_at else "Not checked in"
        button = f'<a href="/admin/checkin/{c.id}" style="background:#00C4B4;color:white;padding:8px 16px;border-radius:6px;text-decoration:none">Check-in</a>' if not c.check_in_at else "Checked In"
        rows += f"""
        <tr>
          <td>{c.id}</td>
          <td>{c.first_name} {c.last_name}</td>
          <td>{c.business_name or '-'}</td>
          <td>{c.email}</td>
          <td>{c.phone}</td>
          <td>{c.created_at.strftime("%Y-%m-%d %H:%M")}</td>
          <td>{check_in}</td>
          <td>{button}</td>
        </tr>
        """

    return HTMLResponse(f"""
    <style>
      body {{font-family:'Segoe UI',sans-serif;background:#1e1e1e;color:#e0e0e0;margin:0;padding:20px}}
      .header {{background:#000;color:white;padding:20px;text-align:center;border-radius:12px}}
      .content {{max-width:1200px;margin:auto}}
      table {{width:100%;border-collapse:collapse;margin-top:30px;background:#2a2a2a;box-shadow:0 4px 10px rgba(0,0,0,0.5)}}
      th {{background:#00C4B4;color:white;padding:15px}}
      td {{padding:15px;border-bottom:1px solid #444}}
      tr:hover {{background:#3a3a3a}}
      .add-customer {{background:#00C4B4;color:white;padding:18px;font-size:22px;border:none;border-radius:10px;width:100%;margin-top:20px;cursor:pointer}}
    </style>
    <div class="header">
      <h1>QCR Admin Dashboard</h1>
    </div>
    <div class="content">
      <h2>All Customers</h2>
      <form action="/create-customer" method="post">
        <input name="first_name" placeholder="First Name" required>
        <input name="last_name" placeholder="Last Name" required>
        <input name="business_name" placeholder="Business Name (optional)">
        <input name="email" type="email" placeholder="Email" required>
        <input name="phone" placeholder="Phone Number" required>
        <button type="submit" class="add-customer">Add Customer</button>
      </form>
      <table>
        <tr><th>ID</th><th>Name</th><th>Business</th><th>Email</th><th>Phone</th><th>Created</th><th>Check-in</th><th>Action</th></tr>
        {rows or "<tr><td colspan='8'>No customers yet</td></tr>"}
      </table>
      <p style="text-align:center;margin-top:50px">
        <a href="/login" style="color:#00C4B4">Logout</a>
      </p>
    </div>
    """)

@app.post("/create-customer")
async def create_customer(
    first_name: str = Form(...),
    last_name: str = Form(...),
    business_name: str = Form(""),
    email: str = Form(...),
    phone: str = Form(...)
):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO customers (first_name, last_name, business_name, email, phone)
            VALUES (:first, :last, :business, :email, :phone)
        """), {
            "first": first_name,
            "last": last_name,
            "business": business_name,
            "email": email,
            "phone": phone
        })
        conn.commit()

    return RedirectResponse("/admin", status_code=303)

@app.get("/admin/checkin/{id}")
async def checkin(id: int):
    with engine.connect() as conn:
        conn.execute(text("""
            UPDATE customers SET check_in_at = CURRENT_TIMESTAMP WHERE id = :id
        """), {"id": id})
        conn.commit()

    # Optional: Send WhatsApp or email to customer here

    return RedirectResponse("/admin", status_code=303)
