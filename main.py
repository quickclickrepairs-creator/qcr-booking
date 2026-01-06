from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/admin")
async def admin(request: Request):
    return HTMLResponse("""
    <h1 style="text-align:center;color:#00C4B4">QCR Admin Dashboard</h1>
    <h2 style="text-align:center">Welcome!</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;margin:30px">
      <a href="/new-customer" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;text-align:center">+ New Customer</a>
      <a href="/new-ticket" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;text-align:center">+ New Ticket</a>
      <a href="/new-checkin" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;text-align:center">+ New Check In</a>
      <a href="/new-invoice" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;text-align:center">+ New Invoice</a>
      <a href="/new-estimate" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;text-align:center">+ New Estimate</a>
    </div>
    <h2 style="text-align:center">REMINDERS</h2>
    <p style="text-align:center">No reminders yet</p>
    """)

@app.get("/new-customer")
async def new_customer(request: Request):
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Customer Form</h1><p style='text-align:center'>Form coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/new-ticket")
async def new_ticket(request: Request):
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Ticket Form</h1><p style='text-align:center'>Full repair form coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/new-checkin")
async def new_checkin(request: Request):
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Check In Form</h1><p style='text-align:center'>Form coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/new-invoice")
async def new_invoice(request: Request):
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Invoice Form</h1><p style='text-align:center'>Form coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/new-estimate")
async def new_estimate(request: Request):
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Estimate Form</h1><p style='text-align:center'>Form coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")
