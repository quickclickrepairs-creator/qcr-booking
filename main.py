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
    return HTMLResponse("""
    <h1 style="color:#00C4B4;text-align:center;margin-top:100px">+ New Customer</h1>
    <p style="text-align:center;font-size:24px">Customer form coming soon</p>
    <p style="text-align:center"><a href="/admin">← Back to Dashboard</a></p>
    """)

@app.get("/new-ticket")
async def new_ticket(request: Request):
    return HTMLResponse("""
    <h1 style="color:#00C4B4;text-align:center;margin-top:100px">+ New Ticket</h1>
    <p style="text-align:center;font-size:24px">Full repair form coming soon</p>
    <p style="text-align:center"><a href="/admin">← Back to Dashboard</a></p>
    """)

@app.get("/new-checkin")
async def new_checkin(request: Request):
    return HTMLResponse("""
    <h1 style="color:#00C4B4;text-align:center;margin-top:100px">+ New Check In</h1>
    <p style="text-align:center;font-size:24px">Check in form coming soon</p>
    <p style="text-align:center"><a href="/admin">← Back to Dashboard</a></p>
    """)

@app.get("/new-invoice")
async def new_invoice(request: Request):
    return HTMLResponse("""
    <h1 style="color:#00C4B4;text-align:center;margin-top:100px">+ New Invoice</h1>
    <p style="text-align:center;font-size:24px">Invoice form coming soon</p>
    <p style="text-align:center"><a href="/admin">← Back to Dashboard</a></p>
    """)

@app.get("/new-estimate")
async def new_estimate(request: Request):
    return HTMLResponse("""
    <h1 style="color:#00C4B4;text-align:center;margin-top:100px">+ New Estimate</h1>
    <p style="text-align:center;font-size:24px">Estimate form coming soon</p>
    <p style="text-align:center"><a href="/admin">← Back to Dashboard</a></p>
    """)

@app.get("/organizations")
async def organizations():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>Organizations</h1><p style='text-align:center'>Coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/invoices")
async def invoices():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>Invoices</h1><p style='text-align:center'>Coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/customer-purchases")
async def customer_purchases():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>Customer Purchases</h1><p style='text-align:center'>Coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/refurbs")
async def refurbs():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>Refurbs</h1><p style='text-align:center'>Coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/tickets")
async def tickets():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>Tickets</h1><p style='text-align:center'>Coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/parts")
async def parts():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>Parts</h1><p style='text-align:center'>Coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/more")
async def more():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>More</h1><p style='text-align:center'>Coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")
EOF
