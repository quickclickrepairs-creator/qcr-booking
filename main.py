from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, text
from datetime import datetime

app = FastAPI()

# Database (Render provides DATABASE_URL env var)
import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://qcruser:Quick@Sp-456782@localhost/qcrdb")
engine = create_engine(DATABASE_URL)

# Create bookings table if not exists
with engine.connect() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS bookings (
        id SERIAL PRIMARY KEY,
        customer_name VARCHAR(255),
        customer_email VARCHAR(255),
        customer_phone VARCHAR(50),
        service_type VARCHAR(255),
        appointment_date VARCHAR(50),
        appointment_time VARCHAR(50),
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """))
    conn.commit()

@app.get("/")
async def home(request: Request):
    return HTMLResponse("""
    <div style="max-width:600px;margin:auto;background:white;padding:40px;border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.2);margin-top:50px">
      <h1 style="text-align:center;color:#00C4B4">Quick Click Repairs</h1>
      <h2 style="text-align:center">Book Your Appointment</h2>
      <form action="/book" method="post">
        <input name="customer_name" placeholder="Full Name" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;border:1px solid #ccc" required>
        <input name="customer_email" type="email" placeholder="Email" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;border:1px solid #ccc" required>
        <input name="customer_phone" placeholder="Phone Number" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;border:1px solid #ccc" required>
        <select name="service_type" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;border:1px solid #ccc" required>
          <option value="">Select Service</option>
          <option>Laptop Repair</option>
          <option>Desktop/PC Repair</option>
          <option>Screen Replacement</option>
          <option>Virus Removal</option>
          <option>Data Recovery</option>
          <option>Other</option>
        </select>
        <input name="appointment_date" type="date" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;border:1px solid #ccc" required>
        <select name="appointment_time" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;border:1px solid #ccc" required>
          <option value="">Preferred Time</option>
          <option>09:00 – 10:00</option>
          <option>10:00 – 11:00</option>
          <option>11:00 – 12:00</option>
          <option>13:00 – 14:00</option>
          <option>14:00 – 15:00</option>
          <option>15:00 – 16:00</option>
          <option>16:00 – 17:00</option>
        </select>
        <textarea name="description" rows="4" placeholder="Describe the problem (optional)" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;border:1px solid #ccc"></textarea>
        <button type="submit" style="background:#00C4B4;color:white;padding:18px;font-size:22px;border:none;border-radius:10px;width:100%;cursor:pointer">BOOK APPOINTMENT</button>
      </form>
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
    # Save to database
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO bookings (customer_name, customer_email, customer_phone, service_type, appointment_date, appointment_time, description)
            VALUES (:name, :email, :phone, :service, :date, :time, :desc)
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
    <div style="max-width:600px;margin:auto;background:white;padding:40px;border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.2);margin-top:50px">
      <h1 style="color:green;text-align:center">Appointment Booked!</h1>
      <h2 style="text-align:center">Thank you {customer_name}</h2>
      <p style="text-align:center;font-size:24px">
        Service: {service_type}<br>
        Date: {appointment_date}<br>
        Time: {appointment_time}<br>
        We will contact you on {customer_phone}
      </p>
      <p style="text-align:center;margin-top:50px">
        <a href="/" style="color:#00C4B4">← Book Another</a> | <a href="/admin" style="color:#00C4B4">Admin Dashboard</a>
      </p>
    </div>
    """)

@app.get("/admin")
async def admin():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, customer_name, customer_email, customer_phone, service_type, appointment_date, appointment_time, description, created_at FROM bookings ORDER BY created_at DESC"))
        bookings = result.fetchall()
    rows = ""
    for b in bookings:
        rows += f"<tr><td>{b.id}</td><td>{b.customer_name}</td><td>{b.customer_email}</td><td>{b.customer_phone}</td><td>{b.service_type}</td><td>{b.appointment_date}</td><td>{b.appointment_time}</td><td>{b.description or ''}</td><td>{b.created_at}</td></tr>"
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>QCR – Admin Dashboard</title>
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
            <li><a href="#">Organizations</a></li>
            <li><a href="#">Invoices</a></li>
            <li><a href="#">Customer Purchases</a></li>
            <li><a href="#">Refurbs</a></li>
            <li><a href="#">Tickets</a></li>
            <li><a href="#">Parts</a></li>
            <li><a href="#">More</a></li>
          </ul>
        </nav>
        <div class="content">
          <div class="welcome">Welcome!</div>
          <div class="get-started">
            <a href="#" class="btn"><span class="icon">👤</span> + New Customer</a>
            <a href="#" class="btn"><span class="icon">✔</span> + New Ticket</a>
            <a href="#" class="btn"><span class="icon">📱</span> + New Check In</a>
            <a href="#" class="btn"><span class="icon">🛒</span> + New Invoice</a>
            <a href="#" class="btn"><span class="icon">📄</span> + New Estimate</a>
          </div>
          <div class="reminders">
            <h2>All Bookings ({len(bookings)})</h2>
            <table>
              <tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Service</th><th>Date</th><th>Time</th><th>Description</th><th>Booked At</th></tr>
              {rows or "<tr><td colspan='9' style='text-align:center'>No bookings yet</td></tr>"}
            </table>
          </div>
        </div>
      </div>
    </body>
    </html>
    """)
