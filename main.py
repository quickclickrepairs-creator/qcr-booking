from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import create_engine, text
from datetime import datetime
import os

app = FastAPI()

# Database (use Render DATABASE_URL in production)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://qcruser:Quick@Sp-456782@localhost/qcrdb")
engine = create_engine(DATABASE_URL)

# Create table if missing
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS bookings (
            id SERIAL PRIMARY KEY,
            customer_name VARCHAR(255) NOT NULL,
            customer_email VARCHAR(255) NOT NULL,
            customer_phone VARCHAR(50) NOT NULL,
            service_type VARCHAR(255) NOT NULL,
            appointment_date VARCHAR(50) NOT NULL,
            appointment_time VARCHAR(50) NOT NULL,
            description TEXT,
            created_by VARCHAR(100),  -- who created it (staff name)
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    conn.commit()

# Simple basic auth for staff (change username/password in production!)
security = HTTPBasic()

def verify_staff(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "staff"
    correct_password = "qcrstaff123"  # CHANGE THIS!
    if credentials.username == correct_username and credentials.password == correct_password:
        return credentials.username
    raise HTTPException(status_code=401, detail="Invalid staff credentials")

# Public page — no booking form, only message
@app.get("/")
async def public_page():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Quick Click Repairs - Booking</title>
      <style>
        body { font-family: Arial, sans-serif; background: #1e1e1e; color: #e0e0e0; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; text-align: center; }
        .box { max-width: 600px; padding: 40px; background: #2a2a2a; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h1 { color: #00C4B4; margin-bottom: 20px; }
        p { font-size: 20px; line-height: 1.5; margin: 20px 0; }
        a { color: #00C4B4; text-decoration: none; font-weight: bold; }
        a:hover { text-decoration: underline; }
      </style>
    </head>
    <body>
      <div class="box">
        <h1>Online Booking Disabled</h1>
        <p>We are now accepting appointments **only in-store**.</p>
        <p>Please visit us at the shop or call us to schedule a repair slot.</p>
        <p><strong>Quick Click Repairs</strong><br>
           Unit 18, 9-19 Rose Road<br>
           Southampton, Hampshire SO14 0TE<br>
           Phone: 023 8036 1277</p>
        <p style="margin-top: 40px;">
          <a href="/admin">Staff / Admin Login →</a>
        </p>
      </div>
    </body>
    </html>
    """)

# Staff-only booking form (inside admin — login required)
@app.get("/admin/new-booking")
async def staff_booking_form(staff: str = Depends(verify_staff)):
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Staff - New Booking</title>
      <style>
        body {{ font-family: Arial, sans-serif; background: #1e1e1e; color: #e0e0e0; margin: 0; padding: 40px; }}
        .container {{ max-width: 700px; margin: auto; background: #2a2a2a; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
        h1 {{ color: #00C4B4; text-align: center; }}
        input, select, textarea {{ width: 100%; padding: 14px; margin: 10px 0; border-radius: 8px; border: 1px solid #444; background: #333; color: white; font-size: 16px; }}
        button {{ background: #00C4B4; color: white; padding: 18px; font-size: 20px; border: none; border-radius: 10px; width: 100%; cursor: pointer; }}
        button:hover {{ background: #00a89a; }}
        .back {{ text-align: center; margin-top: 30px; }}
        .back a {{ color: #00C4B4; font-size: 18px; text-decoration: none; }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>New Booking (Staff)</h1>
        <form action="/admin/create-booking" method="post">
          <input name="customer_name" placeholder="Customer Full Name" required>
          <input name="customer_email" type="email" placeholder="Customer Email" required>
          <input name="customer_phone" placeholder="Customer Phone Number" required>
          <select name="service_type" required>
            <option value="">Select Service</option>
            <option>Laptop Repair</option>
            <option>Phone Repair</option>
            <option>Tablet Repair</option>
            <option>PC Repair</option>
            <option>Other</option>
          </select>
          <input name="appointment_date" type="date" required>
          <input name="appointment_time" type="time" required>
          <textarea name="description" rows="4" placeholder="Issue / Notes"></textarea>
          <input type="hidden" name="created_by" value="{staff}">
          <button type="submit">CREATE BOOKING</button>
        </form>
        <div class="back">
          <a href="/admin">← Back to Dashboard</a>
        </div>
      </div>
    </body>
    </html>
    """)

@app.post("/admin/create-booking")
async def create_staff_booking(
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    customer_phone: str = Form(...),
    service_type: str = Form(...),
    appointment_date: str = Form(...),
    appointment_time: str = Form(...),
    description: str = Form(""),
    created_by: str = Form(...)
):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO bookings (customer_name, customer_email, customer_phone, service_type, appointment_date, appointment_time, description, created_by)
            VALUES (:name, :email, :phone, :service, :date, :time, :desc, :by)
        """), {
            "name": customer_name,
            "email": customer_email,
            "phone": customer_phone,
            "service": service_type,
            "date": appointment_date,
            "time": appointment_time,
            "desc": description,
            "by": created_by
        })
        conn.commit()

    return HTMLResponse(f"""
    <div style="max-width:600px;margin:auto;background:#2a2a2a;padding:40px;border-radius:15px;color:#e0e0e0;text-align:center">
      <h1 style="color:#00C4B4">Booking Created Successfully!</h1>
      <p style="font-size:22px">
        Customer: {customer_name}<br>
        Service: {service_type}<br>
        Date/Time: {appointment_date} {appointment_time}<br>
        Created by: {created_by}
      </p>
      <p style="margin-top:40px">
        <a href="/admin" style="color:#00C4B4;font-size:20px">← Back to Dashboard</a>
      </p>
    </div>
    """)

@app.get("/admin")
async def admin_dashboard(credentials: str = Depends(verify_staff)):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM bookings ORDER BY created_at DESC"))
        bookings = result.fetchall()

    rows = ""
    for b in bookings:
        rows += f"""
        <tr>
          <td>{b.id}</td>
          <td>{b.customer_name}</td>
          <td>{b.customer_email}</td>
          <td>{b.customer_phone}</td>
          <td>{b.service_type}</td>
          <td>{b.appointment_date} {b.appointment_time}</td>
          <td>{b.description or '-'}</td>
          <td>{b.created_by or 'Unknown'}</td>
          <td>{b.created_at}</td>
        </tr>
        """

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Admin Dashboard - Quick Click Repairs</title>
      <style>
        body {{ font-family: Arial, sans-serif; background: #1e1e1e; color: #e0e0e0; margin: 0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: auto; }}
        h1 {{ color: #00C4B4; text-align: center; }}
        .header {{ background: #000; padding: 15px; text-align: center; border-radius: 8px; margin-bottom: 30px; }}
        table {{ width: 100%; border-collapse: collapse; background: #2a2a2a; margin-top: 20px; }}
        th {{ background: #00C4B4; color: black; padding: 12px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #444; }}
        tr:hover {{ background: #333; }}
        .new-booking {{ display: block; margin: 30px auto; background: #00C4B4; color: white; padding: 16px 30px; border: none; border-radius: 8px; font-size: 18px; cursor: pointer; text-decoration: none; text-align: center; width: 300px; }}
        .new-booking:hover {{ background: #00a89a; }}
      </style>
    </head>
    <body>
      <div class="header">
        <h1>Quick Click Repairs - Admin Dashboard</h1>
        <p>Logged in as: {credentials}</p>
      </div>
      <div class="container">
        <h2>All Bookings</h2>
        <a href="/admin/new-booking" class="new-booking">+ Create New Booking</a>
        <table>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Service</th>
            <th>Date & Time</th>
            <th>Notes</th>
            <th>Created By</th>
            <th>Created At</th>
          </tr>
          {rows or '<tr><td colspan="9" style="text-align:center">No bookings yet</td></tr>'}
        </table>
        <p style="text-align:center;margin-top:40px">
          <a href="/admin/new-booking" style="color:#00C4B4">Create New Booking</a> | 
          <a href="/" style="color:#00C4B4">Back to Main Site</a>
        </p>
      </div>
    </body>
    </html>
    """)
