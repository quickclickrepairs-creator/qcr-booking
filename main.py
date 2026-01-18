from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, text
from datetime import datetime
import os

app = FastAPI()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://qcruser:Quick@Sp-456782@localhost/qcrdb")
engine = create_engine(DATABASE_URL)

# Create bookings table if not exists
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS bookings (
            id SERIAL PRIMARY KEY,
            customer_name VARCHAR(255) NOT NULL,
            customer_email VARCHAR(255),
            customer_phone VARCHAR(50) NOT NULL,
            service_type VARCHAR(255) NOT NULL,
            appointment_date VARCHAR(50) NOT NULL,
            appointment_time VARCHAR(50) NOT NULL,
            description TEXT,
            created_by VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    conn.commit()

# Simple staff login (change username/password in production!)
def verify_staff(credentials: dict):
    correct_username = "staff"
    correct_password = "qcrstaff123"  # CHANGE THIS!
    if credentials.get("username") == correct_username and credentials.get("password") == correct_password:
        return credentials["username"]
    raise HTTPException(status_code=401, detail="Invalid staff credentials")

# Public page - disabled message
@app.get("/")
async def public_page():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Quick Click Repairs</title>
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
        <h1>Bookings Only In-Store</h1>
        <p>We no longer accept online bookings.</p>
        <p>Please visit our shop or call us to schedule a repair slot.</p>
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

# Login page
@app.get("/admin")
async def admin_login():
    return HTMLResponse("""
    <div style="max-width:400px;margin:100px auto;background:#2a2a2a;padding:40px;border-radius:15px;text-align:center">
      <h1 style="color:#00C4B4">Staff Login</h1>
      <form action="/admin/dashboard" method="post">
        <input name="username" placeholder="Username" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="password" type="password" placeholder="Password" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <button type="submit" style="background:#00C4B4;color:white;padding:15px;width:100%;border:none;border-radius:8px;cursor:pointer">Login</button>
      </form>
    </div>
    """)

# Handle login
@app.post("/admin/dashboard")
async def login_post(username: str = Form(...), password: str = Form(...)):
    if username == "staff" and password == "qcrstaff123":
        return RedirectResponse("/admin/dashboard", status_code=303)
    return HTMLResponse("<h2 style='color:red;text-align:center'>Wrong credentials</h2><p style='text-align:center'><a href='/admin'>← Try again</a></p>")

# Admin dashboard with bookings list
@app.get("/admin/dashboard")
async def admin_dashboard():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM bookings ORDER BY created_at DESC"))
        bookings = result.fetchall()

    rows = ""
    for b in bookings:
        rows += f"""
        <tr>
          <td>{b[0]}</td>
          <td>{b[1]}</td>
          <td>{b[2]}</td>
          <td>{b[3]}</td>
          <td>{b[4]}</td>
          <td>{b[5]} {b[6]}</td>
          <td>{b[7] or '-'}</td>
          <td>{b[8] or 'Unknown'}</td>
          <td>{b[9]}</td>
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
      </div>
      <div class="container">
        <h2>All Bookings</h2>
        <a href="/admin/new-booking" class="new-booking">+ Create New Booking</a>
        <table>
          <tr>
            <th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Service</th><th>Date & Time</th><th>Notes</th><th>Created By</th><th>Created At</th>
          </tr>
          {rows or '<tr><td colspan="9" style="text-align:center">No bookings yet</td></tr>'}
        </table>
        <p style="text-align:center;margin-top:40px">
          <a href="/admin/new-booking" style="color:#00C4B4">Create New Booking</a> | 
          <a href="/" style="color:#00C4B4">Back to Site</a>
        </p>
      </div>
    </body>
    </html>
    """)

# Staff booking form
@app.get("/admin/new-booking")
async def new_booking():
    return HTMLResponse("""
    <html>
    <head>
      <title>New Booking - Staff</title>
      <style>
        body {font-family:Arial,sans-serif;background:#1e1e1e;color:#e0e0e0;margin:0;padding:40px}
        .container {max-width:700px;margin:auto;background:#2a2a2a;padding:40px;border-radius:15px}
        h1 {color:#00C4B4;text-align:center}
        input, select, textarea {width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white;border:1px solid #444}
        button {background:#00C4B4;color:white;padding:18px;font-size:20px;border:none;border-radius:10px;width:100%;cursor:pointer}
        button:hover {background:#00a89a}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>New Booking (Staff Only)</h1>
        <form action="/admin/create-booking" method="post">
          <input name="customer_name" placeholder="Customer Name" required>
          <input name="customer_phone" placeholder="Phone" required>
          <select name="service_type" required>
            <option value="">Service Type</option>
            <option>Laptop Repair</option>
            <option>Phone Repair</option>
            <option>Other</option>
          </select>
          <input name="appointment_date" type="date" required>
          <input name="appointment_time" type="time" required>
          <textarea name="description" rows="4" placeholder="Notes"></textarea>
          <button type="submit">Create Booking</button>
        </form>
        <p style="text-align:center;margin-top:30px"><a href="/admin/dashboard" style="color:#00C4B4">← Back to Dashboard</a></p>
      </div>
    </body>
    </html>
    """)

@app.post("/admin/create-booking")
async def create_booking(
    customer_name: str = Form(...),
    customer_phone: str = Form(...),
    service_type: str = Form(...),
    appointment_date: str = Form(...),
    appointment_time: str = Form(...),
    description: str = Form("")
):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO bookings (customer_name, customer_phone, service_type, appointment_date, appointment_time, description)
            VALUES (:name, :phone, :service, :date, :time, :desc)
        """), {
            "name": customer_name,
            "phone": customer_phone,
            "service": service_type,
            "date": appointment_date,
            "time": appointment_time,
            "desc": description
        })
        conn.commit()

    return HTMLResponse("""
    <html>
    <body style="font-family:Arial;background:#1e1e1e;color:#e0e0e0;text-align:center;padding:100px">
      <h1 style="color:#00C4B4">Booking Created!</h1>
      <p style="font-size:22px">Booking for {customer_name} saved successfully.</p>
      <p style="margin-top:40px">
        <a href="/admin/dashboard" style="color:#00C4B4">Back to Dashboard</a>
      </p>
    </body>
    </html>
    """)
