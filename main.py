from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("booking.html", {"request": request})

@app.get("/admin")
async def admin(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})

@app.get("/new-customer")
async def new_customer(request: Request):
    return templates.TemplateResponse("new_customer.html", {"request": request})

@app.post("/create-customer")
async def create_customer(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    address: str = Form(""),
    notes: str = Form("")
):
    return HTMLResponse(f"""
    <h1 style="color:green;text-align:center;margin-top:100px">Customer Created!</h1>
    <h2 style="text-align:center">{name}</h2>
    <p style="text-align:center;font-size:24px">
      Email: {email}<br>
      Phone: {phone}<br>
      Address: {address}<br>
      Notes: {notes}
    </p>
    <p style="text-align:center;margin-top:50px">
      <a href="/admin">← Back to Dashboard</a>
    </p>
    """)

@app.get("/new-ticket")
async def new_ticket(request: Request):
    return templates.TemplateResponse("new_ticket.html", {"request": request})

@app.post("/create-ticket")
async def create_ticket(
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    customer_phone: str = Form(...),
    device_type: str = Form(...),
    brand: str = Form(...),
    model: str = Form(...),
    serial: str = Form(""),
    password: str = Form(""),
    faults: list[str] = Form([]),
    other_fault: str = Form(""),
    labour_price: float = Form(45.0),
    parts_price: float = Form(0.0),
    notes: str = Form("")
):
    total = labour_price + parts_price
    all_faults = ", ".join(faults)
    if other_fault:
        all_faults += f", {other_fault}"
    return HTMLResponse(f"""
    <h1 style="color:green;text-align:center;margin-top:100px">Ticket Created!</h1>
    <h2 style="text-align:center">Customer: {customer_name}</h2>
    <p style="text-align:center;font-size:24px">
      Device: {brand} {model} ({device_type})<br>
      Faults: {all_faults}<br>
      Labour: £{labour_price:.2f}<br>
      Parts: £{parts_price:.2f}<br>
      Total: £{total:.2f}
    </p>
    <p style="text-align:center;margin-top:50px">
      <a href="/admin">← Back to Dashboard</a>
    </p>
    """)

@app.get("/new-checkin")
async def new_checkin(request: Request):
    return templates.TemplateResponse("new_checkin.html", {"request": request})

@app.get("/new-invoice")
async def new_invoice(request: Request):
    return templates.TemplateResponse("new_invoice.html", {"request": request})

@app.get("/new-estimate")
async def new_estimate(request: Request):
    return templates.TemplateResponse("new_estimate.html", {"request": request})
