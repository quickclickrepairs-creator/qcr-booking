from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/admin")
async def admin():
    return HTMLResponse("""
    <div style="background:#1e1e1e;color:#e0e0e0;padding:20px;min-height:100vh">
      <header style="background:#000;padding:15px 30px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 4px 10px rgba(0,0,0,0.5)">
        <h1 style="color:#fff;font-size:24px">Quick Click Repairs</h1>
        <input type="text" placeholder="Search all the things" style="background:#333;border-radius:20px;padding:8px 15px;color:white;border:none;width:300px">
        <div style="display:flex;align-items:center;gap:10px">
          <span>Alan ▼</span>
          <img src="https://i.imgur.com/placeholder-user.jpg" alt="User" style="width:40px;height:40px;border-radius:50%">
        </div>
      </header>
      <div style="display:flex">
        <nav style="background:#2a2a2a;padding:20px;min-width:200px">
          <ul style="list-style:none">
            <li style="margin:10px 0"><a href="/organizations" style="color:#aaa;text-decoration:none;font-size:16px;display:block;padding:10px;border-radius:8px">Organizations</a></li>
            <li style="margin:10px 0"><a href="/invoices" style="color:#aaa;text-decoration:none;font-size:16px;display:block;padding:10px;border-radius:8px">Invoices</a></li>
            <li style="margin:10px 0"><a href="/customer-purchases" style="color:#aaa;text-decoration:none;font-size:16px;display:block;padding:10px;border-radius:8px">Customer Purchases</a></li>
            <li style="margin:10px 0"><a href="/refurbs" style="color:#aaa;text-decoration:none;font-size:16px;display:block;padding:10px;border-radius:8px">Refurbs</a></li>
            <li style="margin:10px 0"><a href="/tickets" style="color:#aaa;text-decoration:none;font-size:16px;display:block;padding:10px;border-radius:8px">Tickets</a></li>
            <li style="margin:10px 0"><a href="/parts" style="color:#aaa;text-decoration:none;font-size:16px;display:block;padding:10px;border-radius:8px">Parts</a></li>
            <li style="margin:10px 0"><a href="/more" style="color:#aaa;text-decoration:none;font-size:16px;display:block;padding:10px;border-radius:8px">More</a></li>
          </ul>
        </nav>
        <div style="flex:1;padding:30px">
          <div style="font-size:36px;margin-bottom:40px">Welcome!</div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;margin-bottom:40px">
            <a href="/new-customer" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;font-weight:bold;text-align:center;display:flex;align-items:center;justify-content:center;gap:15px">👤 + New Customer</a>
            <a href="/new-ticket" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;font-weight:bold;text-align:center;display:flex;align-items:center;justify-content:center;gap:15px">✔ + New Ticket</a>
            <a href="/new-checkin" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;font-weight:bold;text-align:center;display:flex;align-items:center;justify-content:center;gap:15px">📱 + New Check In</a>
            <a href="/new-invoice" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;font-weight:bold;text-align:center;display:flex;align-items:center;justify-content:center;gap:15px">🛒 + New Invoice</a>
            <a href="/new-estimate" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;font-weight:bold;text-align:center;display:flex;align-items:center;justify-content:center;gap:15px">📄 + New Estimate</a>
          </div>
          <div style="background:#2a2a2a;padding:25px;border-radius:12px">
            <h2>REMINDERS</h2>
            <table style="width:100%;border-collapse:collapse">
              <tr><th style="background:#00C4B4;color:white;padding:12px;text-align:left">MESSAGE</th><th style="background:#00C4B4;color:white;padding:12px;text-align:left">TIME</th><th style="background:#00C4B4;color:white;padding:12px;text-align:left">TECH</th><th style="background:#00C4B4;color:white;padding:12px;text-align:left">CUSTOMER</th></tr>
              <tr><td>No reminders yet</td><td>-</td><td>-</td><td>-</td></tr>
            </table>
            <button style="margin-top:20px;padding:10px 20px;background:#00C4B4;color:white;border:none;border-radius:8px;cursor:pointer">View All</button>
          </div>
        </div>
      </div>
    </div>
    """)

# All routes for buttons and sidebar (no more Not Found)
@app.get("/new-customer")
async def new_customer():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Customer</h1><p style='text-align:center;font-size:24px'>Customer form coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/new-ticket")
async def new_ticket():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Ticket</h1><p style='text-align:center;font-size:24px'>Full repair form coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/new-checkin")
async def new_checkin():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Check In</h1><p style='text-align:center;font-size:24px'>Check in form coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/new-invoice")
async def new_invoice():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Invoice</h1><p style='text-align:center;font-size:24px'>Invoice form coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

@app.get("/new-estimate")
async def new_estimate():
    return HTMLResponse("<h1 style='color:#00C4B4;text-align:center;margin-top:100px'>+ New Estimate</h1><p style='text-align:center;font-size:24px'>Estimate form coming soon</p><p style='text-align:center'><a href='/admin'>← Back</a></p>")

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
