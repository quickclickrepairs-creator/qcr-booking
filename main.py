from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os

app = FastAPI()

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://qcruser:Quick@Sp-456782@localhost/qcrdb")
print(f"Using DATABASE_URL: {DATABASE_URL}")  # Debug in Render logs

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))  # Test connection
        print("Database connection OK")
except Exception as e:
    print(f"Database connection FAILED: {str(e)}")

# Create table if not exists
try:
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS bookings (
                id SERIAL PRIMARY KEY,
                customer_name VARCHAR(255) NOT NULL,
                customer_phone VARCHAR(50) NOT NULL,
                service_type VARCHAR(255) NOT NULL,
                appointment_date VARCHAR(50) NOT NULL,
                appointment_time VARCHAR(50) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        conn.commit()
        print("Bookings table ready")
except Exception as e:
    print(f"Table creation error: {str(e)}")

@app.get("/")
async def public_page():
    return HTMLResponse("""
    <html>
    <head><title>Quick Click Repairs</title></head>
    <body style="font-family:Arial;background:#1e1e1e;color:#e0e0e0;text-align:center;padding:100px">
      <h1 style="color:#00C4B4">Bookings Only In-Store</h1>
      <p style="font-size:22px">Online booking is disabled.</p>
      <p style="font-size:20px">Please visit the shop or call 023 8036 1277 to schedule.</p>
      <p style="margin-top:60px">
        <a href="/admin" style="color:#00C4B4;font-size:20px">Staff Login →</a>
      </p>
    </body>
    </html>
    """)

@app.get("/admin")
async def admin_login():
    return HTMLResponse("""
    <div style="max-width:400px;margin:100px auto;background:#2a2a2a;padding:40px;border-radius:15px;text-align:center;color:#e0e0e0">
      <h1 style="color:#00C4B4">Staff Login</h1>
      <form action="/admin/login" method="post">
        <input name="username" placeholder="Username" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="password" type="password" placeholder="Password" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <button type="submit" style="background:#00C4B4;color:white;padding:15px;width:100%;border:none;border-radius:8px;cursor:pointer">Login</button>
      </form>
    </div>
    """)

@app.post("/admin/login")
async def admin_login_post(username: str = Form(...), password: str = Form(...)):
    print(f"Login attempt: username={username}")
    if username == "staff" and password == "qcrstaff123":
        print("Login success - redirecting to dashboard")
        return RedirectResponse("/admin/dashboard", status_code=303)
    print("Login failed")
    return HTMLResponse("""
    <div style="max-width:400px;margin:100px auto;background:#2a2a2a;padding:40px;border-radius:15px;text-align:center;color:#e0e0e0">
      <h2 style="color:red">Wrong credentials</h2>
      <p><a href="/admin" style="color:#00C4B4">← Try again</a></p>
    </div>
    """)

@app.get("/admin/dashboard")
async def admin_dashboard():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM bookings ORDER BY created_at DESC"))
            bookings = result.fetchall()
            print(f"Loaded {len(bookings)} bookings")
    except SQLAlchemyError as e:
        print(f"Database query error: {str(e)}")
        bookings = []
    except Exception as e:
        print(f"Unexpected error in dashboard: {str(e)}")
        bookings = []

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
        body {{font-family:Arial,sans-serif;background:#1e1e1e;color:#e0e0e0;margin:0;padding:20px}}
        .container {{max-width:1400px;margin:auto}}
        h1 {{color:#00C4B4;text-align:center}}
        table {{width:100%;border-collapse:collapse;background:#2a2a2a;margin-top:20px}}
        th {{background:#00C4B4;color:black;padding:12px;text-align:left}}
        td {{padding:12px;border-bottom:1px solid #444}}
        tr:hover {{background:#333}}
        .new-booking {{display:block;margin:30px auto;background:#00C4B4;color:white;padding:16px 30px;border:none;border-radius:8px;font-size:18px;cursor:pointer;text-decoration:none;text-align:center;width:300px}}
        .new-booking:hover {{background:#00a89a}}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Admin Dashboard</h1>
        <a href="/admin/new-booking" class="new-booking">+ Create New Booking</a>
        <h2>All Bookings</h2>
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
    try:
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
            print("Booking saved successfully")
    except Exception as e:
        print(f"Booking save error: {str(e)}")
        return HTMLResponse(f"<h2 style='color:red'>Error saving booking: {str(e)}</h2><a href='/admin/new-booking'>← Try again</a>")

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
