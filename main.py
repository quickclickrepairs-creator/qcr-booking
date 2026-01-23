from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# Your existing routes...

# Login page (GET)
@app.get("/admin")
async def admin_login():
    return HTMLResponse("""
    <div style="max-width:400px;margin:100px auto;background:#2a2a2a;padding:40px;border-radius:15px;text-align:center;color:#e0e0e0">
      <h1 style="color:#00C4B4">Staff Login</h1>
      <form action="/admin/login" method="post">
        <input name="username" placeholder="Username" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="password" type="password" placeholder="Password" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <button type="submit" style="background:#00C4B4;color:white;padding:15px;width:100%;border:none;border-radius:8px;cursor:pointer">Login</button>
      </form>
    </div>
    """)

# Login handler (POST) – this fixes the error
@app.post("/admin/login")
async def admin_login_post(username: str = Form(...), password: str = Form(...)):
    # Replace with your real check
    if username == "staff" and password == "qcrstaff123":
        # In real app you'd set a session/cookie here
        return RedirectResponse("/admin/dashboard", status_code=303)
    
    return HTMLResponse("""
    <div style="max-width:400px;margin:100px auto;background:#2a2a2a;padding:40px;border-radius:15px;text-align:center;color:#e0e0e0">
      <h2 style="color:red">Wrong credentials</h2>
      <p><a href="/admin" style="color:#00C4B4">← Try again</a></p>
    </div>
    """)

@app.post("/admin/login")
async def admin_login_post(username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USER and password == ADMIN_PASS:
        return RedirectResponse("/admin/dashboard", status_code=303)
    return HTMLResponse("<h2 style='color:red;text-align:center'>Wrong credentials</h2><p><a href='/admin'>← Try again</a></p>")

@app.get("/admin/dashboard")
async def admin_dashboard():
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
            <li><a href="#">Organizations</a></li>
            <li><a href="#">Invoices</a></li>
            <li><a href="#">Customer Purchases</a></li>
            <li><a href="#">Refurbs</a></li>
            <li><a href="#">Tickets</a></li>
            <li><a href="#">Parts</a></li>
            <li><a href="#">More</a></li>
          </ul>
        </nav>
        <div class="content">
          <div class="welcome">Welcome!</div>
          <div class="get-started">
            <a href="#" class="btn"><span class="icon">👤</span> + New Customer</a>
            <a href="#" class="btn"><span class="icon">✔</span> + New Ticket</a>
            <a href="#" class="btn"><span class="icon">📱</span> + New Check In</a>
            <a href="#" class="btn"><span class="icon">🛒</span> + New Invoice</a>
            <a href="#" class="btn"><span class="icon">📄</span> + New Estimate</a>
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

# Customers table (if not already created)
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            business_name VARCHAR(150),
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            check_in_at TIMESTAMP
        )
    """))
    conn.commit()

# New Customer form (staff only)
@app.get("/admin/new-customer")
async def new_customer_form():
    return HTMLResponse("""
    <div style="max-width:600px;margin:40px auto;background:#2a2a2a;padding:40px;border-radius:15px">
      <h1 style="color:#00C4B4;text-align:center">New Customer</h1>
      <form action="/admin/create-customer" method="post">
        <input name="first_name" placeholder="First Name" required style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <input name="last_name" placeholder="Last Name" required style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <input name="business_name" placeholder="Business Name (optional)" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <input name="email" type="email" placeholder="Email" required style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <input name="phone" placeholder="Phone Number" required style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <button type="submit" style="background:#00C4B4;color:white;padding:18px;font-size:20px;border:none;border-radius:10px;width:100%;cursor:pointer;margin-top:20px">Save Customer</button>
      </form>
      <p style="text-align:center;margin-top:30px"><a href="/admin/dashboard" style="color:#00C4B4">← Back to Dashboard</a></p>
    </div>
    """)

# Create Customer (POST)
@app.post("/admin/create-customer")
async def create_customer(
    first_name: str = Form(...),
    last_name: str = Form(...),
    business_name: str = Form(None),
    email: str = Form(...),
    phone: str = Form(...)
):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO customers (first_name, last_name, business_name, email, phone)
            VALUES (:first, :last, :business, :email, :phone)
        """), {
            "first": first_name,
            "last": last_name,
            "business": business_name,
            "email": email,
            "phone": phone
        })
        conn.commit()
    return RedirectResponse("/admin/dashboard", status_code=303)

# Check-in (GET)
@app.get("/admin/checkin/{customer_id}")
async def checkin(customer_id: int):
    with engine.connect() as conn:
        conn.execute(text("""
            UPDATE customers SET check_in_at = CURRENT_TIMESTAMP WHERE id = :id AND check_in_at IS NULL
        """), {"id": customer_id})
        conn.commit()
    return RedirectResponse("/admin/dashboard", status_code=303)
