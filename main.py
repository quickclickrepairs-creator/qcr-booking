from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

# Booking page (GET) - your form loads here
@app.get("/")
async def home():
    return HTMLResponse("""
    <html>
    <head><title>Book Appointment - Quick Click Repairs</title></head>
    <body style="font-family:Arial;background:#f0f8ff;text-align:center;padding:50px">
      <h1 style="color:#00C4B4">Book Appointment</h1>
      <form action="/book" method="post">
        <input name="customer_name" placeholder="Full Name" required style="width:300px;padding:10px;margin:10px"><br>
        <input name="customer_email" type="email" placeholder="Email" required style="width:300px;padding:10px;margin:10px"><br>
        <input name="customer_phone" placeholder="Phone Number" required style="width:300px;padding:10px;margin:10px"><br>
        <select name="service_type" required style="width:300px;padding:10px;margin:10px">
          <option value="">Select Service</option>
          <option>Screen Repair</option>
          <option>Battery Replacement</option>
          <option>Software Issue</option>
          <option>Other</option>
        </select><br>
        <input name="appointment_date" type="date" required style="width:300px;padding:10px;margin:10px"><br>
        <input name="appointment_time" type="time" required style="width:300px;padding:10px;margin:10px"><br>
        <textarea name="description" placeholder="Description (optional)" style="width:300px;padding:10px;margin:10px"></textarea><br>
        <button type="submit" style="background:#00C4B4;color:white;padding:15px 30px;border:none;border-radius:8px;font-size:18px;cursor:pointer">BOOK APPOINTMENT</button>
      </form>
    </body>
    </html>
    """)

# Booking submission (POST) - this fixes the Not Found
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
    # Success confirmation page
    return HTMLResponse(f"""
    <html>
    <head><title>Booked!</title></head>
    <body style="font-family:Arial;background:#f0f8ff;text-align:center;padding:50px">
      <h1 style="color:green">Appointment Booked!</h1>
      <h2>Thank you {customer_name}!</h2>
      <p style="font-size:24px">
        Service: <strong>{service_type}</strong><br>
        Date: <strong>{appointment_date}</strong><br>
        Time: <strong>{appointment_time}</strong><br>
        We will contact you on <strong>{customer_phone}</strong>
      </p>
      <p style="margin-top:50px">
        <a href="/" style="color:#00C4B4;font-size:20px">← Book Another Appointment</a>
      </p>
    </body>
    </html>
    """)
