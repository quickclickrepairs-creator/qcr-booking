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
        <a href="/new-ticket" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;text-align:center;font-weight:bold">+ New Ticket</a>
        <a href="/new-checkin" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;text-align:center;font-weight:bold">+ New Check In</a>
        <a href="/new-invoice" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;text-align:center;font-weight:bold">+ New Invoice</a>
        <a href="/new-estimate" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;text-align:center;font-weight:bold">+ New Estimate</a>
      </div>
    </div>
    """)

# Real forms for all buttons
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
async def create_customer(name: str = Form(...), email: str = Form(...), phone: str = Form(...), address: str = Form(""), notes: str = Form("")):
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

@app.get("/new-ticket")
async def new_ticket():
    return HTMLResponse("""
    <div style="max-width:900px;margin:auto;background:#2a2a2a;padding:40px;border-radius:15px;color:#e0e0e0">
      <h1 style="text-align:center;color:#00C4B4;margin-bottom:30px">+ New Ticket</h1>
      <form action="/create-ticket" method="post">
        <h2 style="color:#00C4B4">Customer</h2>
        <input name="customer_name" placeholder="Full Name" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="customer_email" type="email" placeholder="Email" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="customer_phone" placeholder="Phone Number" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>

        <h2 style="color:#00C4B4">Device</h2>
        <select name="device_type" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
          <option value="">Select Type</option>
          <option>Laptop</option>
          <option>Phone</option>
          <option>Tablet</option>
          <option>Desktop</option>
          <option>Other</option>
        </select>
        <input name="brand" placeholder="Brand" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="model" placeholder="Model" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="serial" placeholder="Serial/IMEI" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">

        <h2 style="color:#00C4B4">Faults (check all that apply)</h2>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px">
          <label><input type="checkbox" name="faults" value="No Power"> No Power</label>
          <label><input type="checkbox" name="faults" value="Won't Charge"> Won't Charge</label>
          <label><input type="checkbox" name="faults" value="Cracked Screen"> Cracked Screen</label>
          <label><input type="checkbox" name="faults" value="Liquid Damage"> Liquid Damage</label>
          <label><input type="checkbox" name="faults" value="Slow Performance"> Slow Performance</label>
          <label><input type="checkbox" name="faults" value="Virus/Malware"> Virus/Malware</label>
          <label><input type="checkbox" name="faults" value="Other"> Other</label>
        </div>
        <input name="other_fault" placeholder="Describe 'Other' fault" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">

        <h2 style="color:#00C4B4">Accessories</h2>
        <input name="accessories" placeholder="Accessories (charger, case, etc)" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">

        <h2 style="color:#00C4B4">Estimated Repair Cost</h2>
        <input name="estimated_cost" type="number" step="0.01" placeholder="Estimated Cost £" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">

        <button type="submit" style="background:#00C4B4;color:white;padding:18px;font-size:22px;border:none;border-radius:10px;width:100%;margin-top:20px;cursor:pointer">CREATE TICKET</button>
      </form>
      <p style="text-align:center;margin-top:30px"><a href="/admin" style="color:#00C4B4">← Back to Dashboard</a></p>
    </div>
    """)

@app.post("/create-ticket")
async def create_ticket(
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    customer_phone: str = Form(...),
    device_type: str = Form(...),
    brand: str = Form(...),
    model: str = Form(...),
    serial: str = Form(""),
    accessories: str = Form(""),
    estimated_cost: float = Form(0.0)
):
    all_faults = ", ".join(faults)
    if other_fault:
        all_faults += f", {other_fault}"
    return HTMLResponse(f"""
    <div style="max-width:800px;margin:auto;background:#2a2a2a;padding:40px;border-radius:15px;color:#e0e0e0">
      <h1 style="color:green;text-align:center">TICKET CREATED!</h1>
      <h2 style="text-align:center">Customer: {customer_name}</h2>
      <p style="text-align:center;font-size:24px">
        Device: {brand} {model} ({device_type})<br>
        Serial: {serial}<br>
        Faults: {all_faults or 'None specified'}<br>
        Accessories: {accessories or 'None'}<br>
        <strong>Estimated Repair Cost: £{estimated_cost:.2f}</strong>
      </p>
      <p style="text-align:center;margin-top:50px">
        <a href="/admin" style="color:#00C4B4">← Back to Dashboard</a>
      </p>
    </div>
    """)

# Placeholder for other buttons (to avoid Not Found)
@app.get("/new-checkin")
async def new_checkin():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Check In</h1><p style='text-align:center'>Form coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/new-invoice")
async def new_invoice():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Invoice</h1><p style='text-align:center'>Form coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/new-estimate")
async def new_estimate():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Estimate</h1><p style='text-align:center'>Form coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")
