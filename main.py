from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/admin")
async def admin():
    return HTMLResponse("""
    <div style="background:#1e1e1e;color:#e0e0e0;padding:20px;min-height:100vh">
      <h1 style="text-align:center;color:#00C4B4">QCR Admin Dashboard</h1>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;max-width:1200px;margin:auto">
        <a href="/new-customer" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;text-align:center;font-weight:bold">+ New Customer</a>
        <div style="background:#444;color:#888;padding:30px;border-radius:12px;font-size:20px;text-align:center;font-weight:bold">+ New Ticket</div>
        <div style="background:#444;color:#888;padding:30px;border-radius:12px;font-size:20px;text-align:center;font-weight:bold">+ New Check In</div>
        <div style="background:#444;color:#888;padding:30px;border-radius:12px;font-size:20px;text-align:center;font-weight:bold">+ New Invoice</div>
        <div style="background:#444;color:#888;padding:30px;border-radius:12px;font-size:20px;text-align:center;font-weight:bold">+ New Estimate</div>
      </div>
    </div>
    """)

@app.get("/new-customer")
async def new_customer():
    return HTMLResponse("""
    <div style="max-width:600px;margin:auto;background:#2a2a2a;padding:40px;border-radius:15px;color:#e0e0e0">
      <h1 style="text-align:center;color:#00C4B4;margin-bottom:30px">+ New Customer</h1>
      <form action="/create-customer" method="post">
        <input name="name" placeholder="Full Name" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="email" type="email" placeholder="Email" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="phone" placeholder="Phone Number" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="address" placeholder="Address" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <textarea name="notes" rows="4" placeholder="Notes (optional)" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white"></textarea>
        <button type="submit" style="background:#00C4B4;color:white;padding:18px;font-size:22px;border:none;border-radius:10px;width:100%;margin-top:20px;cursor:pointer">SAVE CUSTOMER</button>
      </form>
      <p style="text-align:center;margin-top:30px"><a href="/admin" style="color:#00C4B4">← Back to Dashboard</a></p>
    </div>
    """)

@app.post("/create-customer")
async def create_customer(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    address: str = Form(""),
    notes: str = Form("")
):
    return HTMLResponse(f"""
    <div style="max-width:600px;margin:auto;background:#2a2a2a;padding:40px;border-radius:15px;color:#e0e0e0">
      <h1 style="color:green;text-align:center">Customer Created!</h1>
      <h2 style="text-align:center">{name}</h2>
      <p style="text-align:center;font-size:24px">
        Email: {email}<br>
        Phone: {phone}<br>
        Address: {address or 'Not provided'}<br>
        Notes: {notes or 'None'}
      </p>
      <p style="text-align:center;margin-top:50px">
        <a href="/admin" style="color:#00C4B4">← Back to Dashboard</a>
      </p>
    </div>
    """)
