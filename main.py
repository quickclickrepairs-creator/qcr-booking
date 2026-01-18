from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

# Public booking page (disabled - in-store only message)
@app.get("/")
async def public_page():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Quick Click Repairs</title>
      <style>
        body {font-family:Arial,sans-serif;background:#1e1e1e;color:#e0e0e0;margin:0;padding:0;display:flex;justify-content:center;align-items:center;height:100vh;text-align:center}
        .box {max-width:600px;padding:40px;background:#2a2a2a;border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.5)}
        h1 {color:#00C4B4;margin-bottom:20px}
        p {font-size:20px;line-height:1.5;margin:20px 0}
        a {color:#00C4B4;text-decoration:none;font-weight:bold}
        a:hover {text-decoration:underline}
      </style>
    </head>
    <body>
      <div class="box">
        <h1>Bookings Only In-Store</h1>
        <p>We no longer accept online bookings.</p>
        <p>Please visit our shop or call us to schedule a repair slot.</p>
        <p><strong>Quick Click Repairs</strong><br>
           Unit 18, 9-19 Rose Road<br>
           Southampton, Hampshire SO14 0TE<br>
           Phone: 023 8036 1277</p>
        <p style="margin-top:40px;">
          <a href="/admin">Staff / Admin Login →</a>
        </p>
      </div>
    </body>
    </html>
    """)

# Staff login page
# Staff login page (GET)
@app.get("/admin")
async def admin_login():
    return HTMLResponse("""
    <div style="max-width:400px;margin:100px auto;background:#2a2a2a;padding:40px;border-radius:15px;text-align:center;color:#e0e0e0">
      <h1 style="color:#00C4B4">Staff Login</h1>
      <form action="/admin/login" method="post">
        <input name="username" placeholder="Username" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white;border:1px solid #444" required>
        <input name="password" type="password" placeholder="Password" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white;border:1px solid #444" required>
        <button type="submit" style="background:#00C4B4;color:white;padding:15px;width:100%;border:none;border-radius:8px;cursor:pointer;font-size:18px">Login</button>
      </form>
      <p style="margin-top:20px"><a href="/" style="color:#00C4B4">Back to main site</a></p>
    </div>
    """)

# Handle login (POST)
@app.post("/admin/login")
async def admin_login_post(username: str = Form(...), password: str = Form(...)):
    # Simple check - change these credentials later!
    if username == "staff" and password == "qcrstaff123":
        # In real app you'd use session/cookie here - for now we redirect
        return RedirectResponse("/admin/dashboard", status_code=303)
    return HTMLResponse("""
    <div style="max-width:400px;margin:100px auto;background:#2a2a2a;padding:40px;border-radius:15px;text-align:center;color:#e0e0e0">
      <h2 style="color:red">Wrong credentials</h2>
      <p><a href="/admin" style="color:#00C4B4">← Try again</a></p>
    </div>
    """)

# Admin dashboard
@app.get("/admin/dashboard")
async def admin_dashboard():
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
            <li style="margin:10px 0"><a href="#" style="color:#aaa;text-decoration:none;font-size:16px;display:block;padding:10px;border-radius:8px">Organizations</a></li>
            <li style="margin:10px 0"><a href="#" style="color:#aaa;text-decoration:none;font-size:16px;display:block;padding:10px;border-radius:8px">Invoices</a></li>
            <li style="margin:10px 0"><a href="#" style="color:#aaa;text-decoration:none;font-size:16px;display:block;padding:10px;border-radius:8px">Customer Purchases</a></li>
            <li style="margin:10px 0"><a href="#" style="color:#aaa;text-decoration:none;font-size:16px;display:block;padding:10px;border-radius:8px">Refurbs</a></li>
            <li style="margin:10px 0"><a href="#" style="color:#aaa;text-decoration:none;font-size:16px;display:block;padding:10px;border-radius:8px">Tickets</a></li>
            <li style="margin:10px 0"><a href="#" style="color:#aaa;text-decoration:none;font-size:16px;display:block;padding:10px;border-radius:8px">Parts</a></li>
            <li style="margin:10px 0"><a href="#" style="color:#aaa;text-decoration:none;font-size:16px;display:block;padding:10px;border-radius:8px">More</a></li>
          </ul>
        </nav>
        <div style="flex:1;padding:30px">
          <div style="font-size:36px;margin-bottom:40px">Welcome!</div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;margin-bottom:40px">
            <a href="#" class="btn" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;font-weight:bold;text-align:center;display:flex;align-items:center;justify-content:center;gap:15px">👤 + New Customer</a>
            <a href="#" class="btn" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;font-weight:bold;text-align:center;display:flex;align-items:center;justify-content:center;gap:15px">✔ + New Ticket</a>
            <a href="#" class="btn" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;font-weight:bold;text-align:center;display:flex;align-items:center;justify-content:center;gap:15px">📱 + New Check In</a>
            <a href="#" class="btn" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;font-weight:bold;text-align:center;display:flex;align-items:center;justify-content:center;gap:15px">🛒 + New Invoice</a>
            <a href="#" class="btn" style="background:#00C4B4;color:white;padding:30px;border-radius:12px;text-decoration:none;font-size:20px;font-weight:bold;text-align:center;display:flex;align-items:center;justify-content:center;gap:15px">📄 + New Estimate</a>
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
