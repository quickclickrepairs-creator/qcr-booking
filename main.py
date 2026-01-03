from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("booking.html", {"request": request})

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
    return HTMLResponse(f"""
    <h1 style="color:green;text-align:center;margin-top:100px">Appointment Booked!</h1>
    <h2 style="text-align:center">Thank you {customer_name}</h2>
    <p style="text-align:center;font-size:24px">
      Service: {service_type}<br>
      Date: {appointment_date}<br>
      Time: {appointment_time}<br>
      We will contact you on {customer_phone}
    </p>
    <p style="text-align:center;margin-top:50px">
      <a href="/">← Book Another</a> | <a href="/admin">Admin Dashboard</a>
    </p>
    """)

@app.get("/admin")
async def admin(request: Request):
    return HTMLResponse("""
    <h1 style="text-align:center;color:#00C4B4;margin-top:100px">QCR Admin Dashboard</h1>
    <h2 style="text-align:center">All Bookings</h2>
    <p style="text-align:center;font-size:24px">Real bookings will appear here soon</p>
    <table style="margin:auto;width:80%;border-collapse:collapse">
      <tr style="background:#00C4B4;color:white"><th>Name</th><th>Email</th><th>Phone</th><th>Service</th><th>Date</th><th>Time</th></tr>
      <tr><td>Test Customer</td><td>test@example.com</td><td>07123 456789</td><td>Laptop Repair</td><td>2026-01-05</td><td>10:00 – 11:00</td></tr>
    </table>
    <p style="text-align:center;margin-top:50px"><a href="/">← Back to Booking</a></p>
    """)
