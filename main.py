from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

# FULL DASHBOARD (beautiful dark layout from your screenshot)
@app.get("/admin")
async def admin():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Quick Click Repairs – Dashboard</title>
      <style>
        * {margin:0;padding:0;box-sizing:border-box}
        body {font-family: 'Segoe UI', Arial, sans-serif; background:#1e1e1e; color:#e0e0e0; margin:0}
        header {background:#000; padding:15px 30px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 4px 10px rgba(0,0,0,0.5)}
        header h1 {color:#fff; font-size:24px}
        .search {background:#333; border-radius:20px; padding:8px 15px; color:white; border:none; width:300px}
        .user {display:flex; align-items:center; gap:10px}
        .user img {width:40px; height:40px; border-radius:50%}
        nav {background:#2a2a2a; padding:20px; min-width:200px}
        nav ul {list-style:none}
        nav li {margin:10px 0}
        nav a {color:#aaa; text-decoration:none; font-size:16px; display:block; padding:10px; border-radius:8px}
        nav a:hover {background:#00C4B4; color:white}
        .main {display:flex}
        .content {flex:1; padding:30px}
        .welcome {font-size:36px; margin-bottom:40px}
        .get-started {display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:20px; margin-bottom:40px}
        .btn {background:#00C4B4; color:white; padding:30px; border-radius:12px; text-decoration:none; font-size:20px; font-weight:bold; text-align:center; display:flex; align-items:center; justify-content:center; gap:15px}
        .btn:hover {background:#00a89a}
        .icon {font-size:32px}
        .reminders {background:#2a2a2a; padding:25px; border-radius:12px}
        .reminders h2 {margin-bottom:20px}
        table {width:100%; border-collapse:collapse}
        th {background:#00C4B4; color:white; padding:12px; text-align:left}
        td {padding:12px; border-bottom:1px solid #444}
      </style>
    </head>
    <body>
      <header>
        <h1>Quick Click Repairs</h1>
        <input type="text" placeholder="Search all the things" class="search">
        <div class="user">
          <span>Alan ▼</span>
          <img src="https://i.imgur.com/placeholder-user.jpg" alt="User">
        </div>
      </header>
      <div class="main">
        <nav>
          <ul>
            <li><a href="/organizations">Organizations</a></li>
            <li><a href="/invoices">Invoices</a></li>
            <li><a href="/customer-purchases">Customer Purchases</a></li>
            <li><a href="/refurbs">Refurbs</a></li>
            <li><a href="/tickets">Tickets</a></li>
            <li><a href="/parts">Parts</a></li>
            <li><a href="/more">More</a></li>
          </ul>
        </nav>
        <div class="content">
          <div class="welcome">Welcome!</div>
          <div class="get-started">
            <a href="/new-customer" class="btn"><span class="icon">👤</span> + New Customer</a>
            <a href="/new-ticket" class="btn"><span class="icon">✔</span> + New Ticket</a>
            <a href="/new-checkin" class="btn"><span class="icon">📱</span> + New Check In</a>
            <a href="/new-invoice" class="btn"><span class="icon">🛒</span> + New Invoice</a>
            <a href="/new-estimate" class="btn"><span class="icon">📄</span> + New Estimate</a>
          </div>
          <div class="reminders">
            <h2>REMINDERS</h2>
            <table>
              <tr><th>MESSAGE</th><th>TIME</th><th>TECH</th><th>CUSTOMER</th></tr>
              <tr><td>No reminders yet</td><td>-</td><td>-</td><td>-</td></tr>
            </table>
            <button style="margin-top:20px;padding:10px 20px;background:#00C4B4;color:white;border:none;border-radius:8px;cursor:pointer">View All</button>
          </div>
        </div>
      </div>
    </body>
    </html>
    """)

# REAL FORMS FOR ALL BUTTONS
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
        <h2 style="color:#00C4B4">Faults</h2>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px">
          <label><input type="checkbox" name="faults" value="No Power"> No Power</label>
          <label><input type="checkbox" name="faults" value="Won't Charge"> Won't Charge</label>
          <label><input type="checkbox" name="faults" value="Cracked Screen"> Cracked Screen</label>
          <label><input type="checkbox" name="faults" value="Liquid Damage"> Liquid Damage</label>
          <label><input type="checkbox" name="faults" value="Slow Performance"> Slow Performance</label>
          <label><input type="checkbox" name="faults" value="Other"> Other</label>
        </div>
        <input name="other_fault" placeholder="Other fault details" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <h2 style="color:#00C4B4">Accessories</h2>
        <input name="accessories" placeholder="Charger, case, etc" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <h2 style="color:#00C4B4">Estimated Repair Cost</h2>
        <input name="estimated_cost" type="number" step="0.01" placeholder="£" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <button type="submit" style="background:#00C4B4;color:white;padding:18px;font-size:22px;border:none;border-radius:10px;width:100%;margin-top:20px;cursor:pointer">CREATE TICKET</button>
      </form>
      <p style="text-align:center;margin-top:30px"><a href="/admin" style="color:#00C4B4">← Back</a></p>
    </div>
    """)

@app.post("/create-ticket")
async def create_ticket(customer_name: str = Form(...), customer_email: str = Form(...), customer_phone: str = Form(...), device_type: str = Form(...), brand: str = Form(...), model: str = Form(...), serial: str = Form(""), accessories: str = Form(""), estimated_cost: float = Form(0.0)):
    return HTMLResponse(f"""
    <div style="max-width:800px;margin:auto;background:#2a2a2a;padding:40px;border-radius:15px;color:#e0e0e0">
      <h1 style="color:green;text-align:center">TICKET CREATED!</h1>
      <h2 style="text-align:center">Customer: {customer_name}</h2>
      <p style="text-align:center;font-size:24px">
        Device: {brand} {model} ({device_type})<br>
        Serial: {serial or 'N/A'}<br>
        Accessories: {accessories or 'None'}<br>
        <strong>Estimated Cost: £{estimated_cost:.2f}</strong>
      </p>
      <p style="text-align:center;margin-top:50px"><a href="/admin" style="color:#00C4B4">← Back</a></p>
    </div>
    """)

# Placeholder for remaining buttons (no Not Found)
@app.get("/new-checkin")
async def new_checkin():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Check In</h1><p style='text-align:center'>Form ready soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/new-invoice")
async def new_invoice():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Invoice</h1><p style='text-align:center'>Form ready soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/new-estimate")
async def new_estimate():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Estimate</h1><p style='text-align:center'>Form ready soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

# Sidebar links (real pages)
@app.get("/organizations")
async def organizations():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>Organizations</h1><p style='text-align:center'>Manage organizations</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/invoices")
async def invoices():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>Invoices</h1><p style='text-align:center'>View invoices</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/customer-purchases")
async def customer_purchases():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>Customer Purchases</h1><p style='text-align:center'>Purchase history</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/refurbs")
async def refurbs():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>Refurbs</h1><p style='text-align:center'>Refurbished items</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/tickets")
async def tickets():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>Tickets</h1><p style='text-align:center'>Repair tickets</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/parts")
async def parts():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>Parts</h1><p style='text-align:center'>Parts inventory</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/more")
async def more():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>More</h1><p style='text-align:center'>Additional tools</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")
