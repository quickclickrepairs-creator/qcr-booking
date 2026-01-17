from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, text
import os

app = FastAPI()

# Database connection (use Render DATABASE_URL env var in production)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://qcruser:Quick@Sp-456782@localhost/qcrdb")
engine = create_engine(DATABASE_URL)

# Ensure table exists
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    conn.commit()

@app.get("/")
async def booking_form():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Quick Click Repairs - Book Appointment</title>
      <style>
        body { font-family: Arial, sans-serif; background: #1e1e1e; color: #e0e0e0; margin: 0; padding: 40px; }
        .container { max-width: 600px; margin: auto; background: #2a2a2a; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h1 { text-align: center; color: #00C4B4; }
        input, select, textarea { width: 100%; padding: 14px; margin: 10px 0; border-radius: 8px; border: 1px solid #444; background: #333; color: white; font-size: 16px; }
        button { background: #00C4B4; color: white; padding: 18px; font-size: 20px; border: none; border-radius: 10px; width: 100%; cursor: pointer; }
        button:hover { background: #00a89a; }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Book Appointment</h1>
        <form action="/book" method="post">
          <input name="customer_name" placeholder="Full Name" required>
          <input name="customer_email" type="email" placeholder="Email" required>
          <input name="customer_phone" placeholder="Phone Number" required>
          <select name="service_type" required>
            <option value="">Select Service</option>
            <option>Laptop Repair</option>
            <option>Phone Repair</option>
            <option>Tablet Repair</option>
            <option>PC/Desktop Repair</option>
            <option>Other</option>
          </select>
          <input name="appointment_date" type="date" required>
          <input name="appointment_time" type="time" required>
          <textarea name="description" rows="4" placeholder="Describe the issue (optional)"></textarea>
          <button type="submit">BOOK APPOINTMENT</button>
        </form>
      </div>
    </body>
    </html>
    """)

@app.post("/book")
async def submit_booking(
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

    # Success page
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head><title>Success</title></head>
    <body style="font-family:Arial;background:#1e1e1e;color:#e0e0e0;text-align:center;padding:100px">
      <h1 style="color:#00C4B4">Appointment Booked!</h1>
      <h2>Thank you, {customer_name}!</h2>
      <p style="font-size:22px">
        Service: <strong>{service_type}</strong><br>
        Date: <strong>{appointment_date}</strong><br>
        Time: <strong>{appointment_time}</strong><br>
        Phone: <strong>{customer_phone}</strong>
      </p>
      <p style="margin-top:60px">
        <a href="/" style="color:#00C4B4;font-size:20px">← Book another appointment</a>
      </p>
    </body>
    </html>
    """)

@app.get("/admin")
async def admin():
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
          <td>{b[5]}</td>
          <td>{b[6]}</td>
          <td>{b[7] or ''}</td>
          <td>{b[8]}</td>
        </tr>
        """

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Admin - Quick Click Repairs</title>
      <style>
        body {{ font-family: Arial, sans-serif; background: #1e1e1e; color: #e0e0e0; margin: 0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: auto; }}
        h1 {{ color: #00C4B4; text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 30px; background: #2a2a2a; }}
        th {{ background: #00C4B4; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #444; }}
        tr:hover {{ background: #333; }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Admin - All Bookings</h1>
        <table>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Service</th>
            <th>Date</th>
            <th>Time</th>
            <th>Description</th>
            <th>Booked At</th>
          </tr>
          {rows or '<tr><td colspan="9" style="text-align:center">No bookings yet</td></tr>'}
        </table>
        <p style="text-align:center;margin-top:50px">
          <a href="/" style="color:#00C4B4">← Back to Booking Page</a>
        </p>
      </div>
    </body>
    </html>
    """)
