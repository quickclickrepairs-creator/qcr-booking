from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, text
from datetime import datetime
import os

app = FastAPI()

# Database (Render sets DATABASE_URL automatically)
DATABASE_URL = os.getenv("DATABASE_URL")
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

metadata.create_all(engine)

# Login credentials (change these!)
ADMIN_USER = "alan"
ADMIN_PASS = "qcr123"

@app.get("/")
async def public_page():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Quick Click Repairs</title>
      <style>
        body {font-family:Arial,sans-serif;background:#1e1e1e;color:#e0e0e0;margin:0;padding:0;display:flex;justify-content:center;align-items:center;height:100vh;text-align:center}
        .box {max-width:600px;padding:40px;background:#2a2a2a;border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.5)}
        h1 {color:#00C4B4;margin-bottom:20px}
        p {font-size:20px;line-height:1.5;margin:20px 0}
        a {color:#00C4B4;text-decoration:none;font-weight:bold}
        a:hover {text-decoration:underline}
      </style>
    </head>
    <body>
      <div class="box">
        <h1>Bookings Only In-Store</h1>
        <p>We no longer accept online bookings.</p>
        <p>Please visit our shop or call us to schedule a repair slot.</p>
        <p><strong>Quick Click Repairs</strong><br>
           Unit 18, 9-19 Rose Road<br>
           Southampton, Hampshire SO14 0TE<br>
           Phone: 023 8036 1277</p>
        <p style="margin-top:40px">
          <a href="/admin">Staff / Admin Login →</a>
        </p>
      </div>
    </body>
    </html>
    """)

@app.get("/admin")
async def admin_login():
    return HTMLResponse("""
    <div style="max-width:400px;margin:100px auto;background:#2a2a2a;padding:40px;border-radius:15px;text-align:center">
      <h1 style="color:#00C4B4">Admin Login</h1>
      <form action="/admin/login" method="post">
        <input name="username" placeholder="Username" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="password" type="password" placeholder="Password" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <button type="submit" style="background:#00C4B4;color:white;padding:15px;width:100%;border:none;border-radius:8px;cursor:pointer">Login</button>
      </form>
    </div>
    """)

@app.post("/admin/login")
async def admin_login_post(username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USER and password == ADMIN_PASS:
        return RedirectResponse("/admin/dashboard", status_code=303)
    return HTMLResponse("<h2 style='color:red;text-align:center'>Wrong credentials</h2><p style='text-align:center'><a href='/admin'>← Try again</a></p>")

@app.get("/admin/dashboard")
async def admin_dashboard():
    with engine.connect() as conn:
        c = conn.execute(text("SELECT * FROM customers ORDER BY created_at DESC")).fetchall()
        t = conn.execute(text("SELECT * FROM tickets ORDER BY created_at DESC")).fetchall()

    customer_rows = ''.join(f"<tr><td>{x.id}</td><td>{x.first_name} {x.last_name}</td><td>{x.business_name or ''}</td><td>{x.email}</td><td>{x.phone}</td><td>{x.created_at}</td></tr>" for x in c) or "<tr><td colspan='6'>No customers</td></tr>"
    ticket_rows = ''.join(f"<tr><td>{x.id}</td><td>{x.customer_name}</td><td>{x.device_type}</td><td>£{x.estimated_cost:.2f}</td><td>{x.created_at}</td></tr>" for x in t) or "<tr><td colspan='5'>No tickets</td></tr>"

    return HTMLResponse(f"""
    <style>
      body {{font-family:'Segoe UI',sans-serif;background:#1e1e1e;color:#e0e0e0;margin:0;padding:20px}}
      .header {{background:#000;color:white;padding:20px;text-align:center;border-radius:12px}}
      .content {{max-width:1200px;margin:auto}}
      table {{width:100%;border-collapse:collapse;margin-top:30px;background:#2a2a2a;box-shadow:0 4px 10px rgba(0,0,0,0.5)}}
      th {{background:#00C4B4;color:white;padding:15px}}
      td {{padding:15px;border-bottom:1px solid #444}}
      tr:hover {{background:#3a3a3a}}
      .btn {{background:#00C4B4;color:white;padding:15px;border:none;border-radius:8px;cursor:pointer;font-size:18px;margin:10px}}
    </style>
    <div class="header">
      <h1>QCR Admin Dashboard</h1>
    </div>
    <div class="content">
      <h2 style="text-align:center">Welcome!</h2>
      <div style="text-align:center;margin:40px 0">
        <a href="/admin/new-customer" class="btn">+ New Customer</a>
        <a href="/admin/new-ticket" class="btn">+ New Ticket</a>
      </div>
      <h2>All Customers ({len(c)})</h2>
      <table>
        <tr><th>ID</th><th>Name</th><th>Business</th><th>Email</th><th>Phone</th><th>Created</th></tr>
        {customer_rows}
      </table>
      <h2>All Tickets ({len(t)})</h2>
      <table>
        <tr><th>ID</th><th>Customer</th><th>Device</th><th>Est. Cost</th><th>Created</th></tr>
        {ticket_rows}
      </table>
      <p style="text-align:center;margin-top:50px">
        <a href="/login" style="color:#00C4B4">Logout</a>
      </p>
    </div>
    """)

@app.get("/admin/new-customer")
async def new_customer():
    return HTMLResponse(f"""
    <div style="background:#1e1e1e;color:#e0e0e0;padding:40px">
      <h1 style="text-align:center;color:#00C4B4">New Customer</h1>
      <form action="/admin/create-customer" method="post" style="max-width:600px;margin:auto;background:#2a2a2a;padding:40px;border-radius:12px">
        <input name="first_name" placeholder="First Name" required style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <input name="last_name" placeholder="Last Name" required style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <input name="business_name" placeholder="Business Name (optional)" style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <input name="email" type="email" placeholder="Email" required style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <input name="phone" placeholder="Phone" required style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <button type="submit" style="background:#00C4B4;color:white;padding:15px;width:100%;border:none;border-radius:8px;cursor:pointer">Save Customer</button>
      </form>
      <p style="text-align:center;margin-top:50px"><a href="/admin/dashboard" style="color:#00C4B4">← Back to Dashboard</a></p>
    </div>
    """)

@app.post("/admin/create-customer")
async def create_customer(
    first_name: str = Form(...),
    last_name: str = Form(...),
    business_name: str = Form(""),
    email: str = Form(...),
    phone: str = Form(...)
):
    with engine.connect() as conn:
        conn.execute(customers.insert().values(
            first_name=first_name,
            last_name=last_name,
            business_name=business_name,
            email=email,
            phone=phone
        ))
        conn.commit()
    return RedirectResponse("/admin/new-ticket", status_code=303)

@app.get("/admin/new-ticket")
async def new_ticket():
    return HTMLResponse(f"""
    <div style="background:#1e1e1e;color:#e0e0e0;padding:40px">
      <h1 style="text-align:center;color:#00C4B4">New Ticket</h1>
      <form action="/admin/create-ticket" method="post" style="max-width:800px;margin:auto;background:#2a2a2a;padding:40px;border-radius:12px">
        <input name="customer_name" placeholder="Customer Name" style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="customer_email" type="email" placeholder="Email" style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="customer_phone" placeholder="Phone" style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <select name="device_type" style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
          <option value="">Device Type</option>
          <option>Laptop</option>
          <option>Phone</option>
          <option>Tablet</option>
          <option>Desktop</option>
          <option>Other</option>
        </select>
        <input name="brand" placeholder="Brand" style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="model" placeholder="Model" style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="serial" placeholder="Serial/IMEI" style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <select name="faults" style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
          <option value="">Select Fault</option>
          <option>Screen Repair</option>
          <option>Anti Virus</option>
          <option>No Power</option>
          <option>Won't Charge</option>
          <option>Cracked Screen</option>
          <option>Liquid Damage</option>
          <option>Slow Performance</option>
          <option>Other</option>
        </select>
        <input name="other_fault" placeholder="Other Fault Details" style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <input name="accessories" placeholder="Accessories (charger, case, etc)" style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <input name="estimated_cost" type="number" step="0.01" placeholder="Estimated Cost (£)" style="width:100%;padding:15px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <button type="submit" style="background:#00C4B4;color:white;padding:15px;width:100%;border:none;border-radius:8px;cursor:pointer">Create Ticket</button>
      </form>
      <p style="text-align:center;margin-top:50px"><a href="/admin" style="color:#00C4B4">← Back to Dashboard</a></p>
    </div>
    """)

@app.post("/admin/create-ticket")
async def create_ticket(
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    customer_phone: str = Form(...),
    device_type: str = Form(...),
    brand: str = Form(...),
    model: str = Form(...),
    serial: str = Form(""),
    faults: str = Form(...),
    other_fault: str = Form(""),
    accessories: str = Form(""),
    estimated_cost: float = Form(0.0)
):
    with engine.connect() as conn:
        conn.execute(tickets.insert().values(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            device_type=device_type,
            brand=brand,
            model=model,
            serial=serial,
            faults=faults,
            other_fault=other_fault,
            accessories=accessories,
            estimated_cost=estimated_cost
        ))
        conn.commit()
    return RedirectResponse("/admin", status_code=303)
