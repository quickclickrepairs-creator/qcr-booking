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
):
    return HTMLResponse(f"""
    <h1 style="color:green;text-align:center;margin-top:100px">BOOKING CONFIRMED!</h1>
    <h2 style="text-align:center">Thank you {customer_name}</h2>
    <p style="text-align:center;font-size:24px">
      Service: {service_type}<br>
      Date: {appointment_date}<br>
      Time: {appointment_time}<br>
      Phone: {customer_phone}<br>
      Email: {customer_email}
    </p>
    <p style="text-align:center;margin-top:50px">
      <a href="/">← Book Another</a>
    </p>
    """)
