import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Request, Form, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/repairshop")
print(f"[DEBUG] Connecting to database: {DATABASE_URL[:20]}...")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    business_name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    check_in_at = Column(DateTime, nullable=True)

# Create tables
try:
    Base.metadata.create_all(bind=engine)
    print("[DEBUG] Database tables created successfully")
except Exception as e:
    print(f"[ERROR] Failed to create tables: {e}")

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Session management (simple in-memory for demo)
sessions = {}

def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    print(f"[DEBUG] Checking session - session_id: {session_id}, active sessions: {len(sessions)}")
    if not session_id or session_id not in sessions:
        print(f"[DEBUG] Session not found or invalid")
        return None
    print(f"[DEBUG] Valid session found for user: {sessions[session_id]}")
    return sessions[session_id]

def require_auth(request: Request):
    user = get_current_user(request)
    if not user:
        print("[DEBUG] Auth required but no valid session, redirecting to login")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user

# Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quick Click Repairs</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: #222;
                padding: 60px 80px;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.5);
                text-align: center;
                max-width: 600px;
            }
            h1 {
                color: #00C4B4;
                font-size: 2.5em;
                margin-bottom: 30px;
                font-weight: bold;
            }
            p {
                color: #ccc;
                font-size: 1.3em;
                line-height: 1.6;
                margin: 20px 0;
            }
            .phone {
                color: #00C4B4;
                font-weight: bold;
                font-size: 1.5em;
                margin-top: 20px;
            }
            .staff-link {
                margin-top: 40px;
                padding-top: 30px;
                border-top: 1px solid #444;
            }
            .staff-link a {
                color: #00C4B4;
                text-decoration: none;
                font-size: 0.9em;
            }
            .staff-link a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Quick Click Repairs</h1>
            <p>Bookings are only accepted in-store.</p>
            <p>Please visit us or call</p>
            <div class="phone">023 8036 1277</div>
            <p style="font-size: 1.1em; margin-top: 30px;">to schedule.</p>
            <div class="staff-link">
                <a href="/login">Staff Login</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=302)
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Staff Login - Quick Click Repairs</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background: #1a1a1a;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .login-container {
                background: #222;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.5);
                width: 100%;
                max-width: 400px;
            }
            h1 {
                color: #00C4B4;
                text-align: center;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                color: #ccc;
                margin-bottom: 8px;
                font-size: 14px;
            }
            input {
                width: 100%;
                padding: 12px;
                background: #333;
                border: 1px solid #444;
                border-radius: 5px;
                color: #fff;
                font-size: 14px;
                box-sizing: border-box;
            }
            input:focus {
                outline: none;
                border-color: #00C4B4;
            }
            button {
                width: 100%;
                padding: 12px;
                background: #00C4B4;
                border: none;
                border-radius: 5px;
                color: #000;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 10px;
            }
            button:hover {
                background: #00d4c4;
            }
            .error {
                color: #ff6b6b;
                text-align: center;
                margin-bottom: 15px;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>Staff Login</h1>
            <form method="post" action="/login">
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    print(f"[DEBUG] Login attempt - username: {username}")
    
    if username == "staff" and password == "qcrstaff123":
        session_id = f"session_{datetime.utcnow().timestamp()}"
        sessions[session_id] = {"username": username}
        print(f"[DEBUG] Login successful - session_id: {session_id}")
        print(f"[DEBUG] Total active sessions: {len(sessions)}")
        
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=86400,
            samesite="lax"
        )
        return response
    
    print("[DEBUG] Login failed - invalid credentials")
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login Failed</title>
        <meta http-equiv="refresh" content="2;url=/login">
        <style>
            body {
                background: #1a1a1a;
                color: #ff6b6b;
                font-family: Arial, sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .message {
                text-align: center;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <div class="message">Invalid credentials. Redirecting...</div>
    </body>
    </html>
    """, status_code=401)

@app.get("/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        del sessions[session_id]
        print(f"[DEBUG] Session {session_id} logged out")
    
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="session_id")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user = Depends(require_auth)):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - Quick Click Repairs</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: Arial, sans-serif;
                background: #1a1a1a;
                color: #fff;
            }
            .header {
                background: #222;
                padding: 15px 30px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: 2px solid #00C4B4;
            }
            .logo {
                font-size: 20px;
                font-weight: bold;
                color: #00C4B4;
            }
            .search-bar {
                flex: 1;
                max-width: 500px;
                margin: 0 30px;
            }
            .search-bar input {
                width: 100%;
                padding: 10px 15px;
                background: #333;
                border: 1px solid #444;
                border-radius: 5px;
                color: #fff;
            }
            .user-info {
                display: flex;
                align-items: center;
                gap: 10px;
                color: #ccc;
            }
            .avatar {
                width: 35px;
                height: 35px;
                background: #00C4B4;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #000;
                font-weight: bold;
            }
            .container {
                display: flex;
                min-height: calc(100vh - 63px);
            }
            .sidebar {
                width: 220px;
                background: #222;
                padding: 20px 0;
                border-right: 1px solid #333;
            }
            .sidebar a {
                display: block;
                padding: 12px 25px;
                color: #ccc;
                text-decoration: none;
                transition: all 0.2s;
            }
            .sidebar a:hover, .sidebar a.active {
                background: #00C4B4;
                color: #000;
                font-weight: bold;
            }
            .main-content {
                flex: 1;
                padding: 30px;
            }
            h1 {
                color: #00C4B4;
                margin-bottom: 30px;
                font-size: 32px;
            }
            h2 {
                color: #00C4B4;
                margin: 30px 0 20px 0;
                font-size: 20px;
            }
            .get-started {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }
            .action-btn {
                background: #00C4B4;
                color: #000;
                padding: 40px 20px;
                border-radius: 8px;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.2s;
                text-decoration: none;
                display: block;
            }
            .action-btn:hover {
                background: #00d4c4;
                transform: translateY(-2px);
            }
            .card {
                background: #222;
                border-radius: 8px;
                padding: 25px;
                border: 1px solid #333;
            }
            .card h3 {
                color: #00C4B4;
                margin-bottom: 15px;
                font-size: 18px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }
            th {
                background: #333;
                padding: 12px;
                text-align: left;
                color: #00C4B4;
                font-weight: bold;
                border-bottom: 2px solid #00C4B4;
            }
            td {
                padding: 12px;
                border-bottom: 1px solid #333;
                color: #ccc;
            }
            .empty-message {
                text-align: center;
                color: #888;
                padding: 30px;
                font-style: italic;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">Quick Click Repairs</div>
            <div class="search-bar">
                <input type="text" placeholder="Search...">
            </div>
            <div class="user-info">
                <span>Alan ▼</span>
                <div class="avatar">A</div>
            </div>
        </div>
        <div class="container">
            <div class="sidebar">
                <a href="/dashboard" class="active">Dashboard</a>
                <a href="/customers">Customers</a>
                <a href="#">Organizations</a>
                <a href="#">Invoices</a>
                <a href="#">Customer Purchases</a>
                <a href="#">Refurbs</a>
                <a href="#">Tickets</a>
                <a href="#">Parts</a>
                <a href="#">Inventory</a>
                <a href="#">Purchase Orders</a>
                <a href="#">POS</a>
                <a href="#">Reports</a>
                <a href="#">Admin</a>
                <a href="#">Help</a>
                <a href="/logout">Logout</a>
            </div>
            <div class="main-content">
                <h1>Welcome!</h1>
                
                <h2>Get Started</h2>
                <div class="get-started">
                    <a href="/customers/new" class="action-btn">+ New Customer</a>
                    <a href="#" class="action-btn">+ New Ticket</a>
                    <a href="#" class="action-btn">+ New Check In</a>
                    <a href="#" class="action-btn">+ New Invoice</a>
                    <a href="#" class="action-btn">+ New Estimate</a>
                </div>
                
                <div class="card">
                    <h3>REMINDERS</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>MESSAGE</th>
                                <th>TIME</th>
                                <th>TECH</th>
                                <th>CUSTOMER</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td colspan="4" class="empty-message">No reminders yet</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/customers", response_class=HTMLResponse)
async def customers_list(request: Request, user = Depends(require_auth), db: Session = Depends(get_db)):
    try:
        customers = db.query(Customer).order_by(Customer.created_at.desc()).all()
        print(f"[DEBUG] Fetched {len(customers)} customers from database")
    except Exception as e:
        print(f"[ERROR] Failed to fetch customers: {e}")
        customers = []
    
    rows_html = ""
    if customers:
        for customer in customers:
            check_in_display = customer.check_in_at.strftime("%Y-%m-%d %H:%M") if customer.check_in_at else "Not checked in"
            check_in_btn = "" if customer.check_in_at else f'<form method="post" action="/customers/{customer.id}/checkin" style="display:inline;"><button type="submit" style="background:#00C4B4;color:#000;border:none;padding:6px 12px;border-radius:4px;cursor:pointer;font-weight:bold;">Check-in</button></form>'
            
            rows_html += f"""
            <tr>
                <td>{customer.id}</td>
                <td>{customer.first_name} {customer.last_name}</td>
                <td>{customer.business_name or '-'}</td>
                <td>{customer.email}</td>
                <td>{customer.phone}</td>
                <td>{customer.created_at.strftime("%Y-%m-%d %H:%M")}</td>
                <td>{check_in_display}</td>
                <td>{check_in_btn}</td>
            </tr>
            """
    else:
        rows_html = '<tr><td colspan="8" class="empty-message">No customers yet. Add your first customer!</td></tr>'
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Customers - Quick Click Repairs</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: Arial, sans-serif;
                background: #1a1a1a;
                color: #fff;
            }}
            .header {{
                background: #222;
                padding: 15px 30px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: 2px solid #00C4B4;
            }}
            .logo {{
                font-size: 20px;
                font-weight: bold;
                color: #00C4B4;
            }}
            .search-bar {{
                flex: 1;
                max-width: 500px;
                margin: 0 30px;
            }}
            .search-bar input {{
                width: 100%;
                padding: 10px 15px;
                background: #333;
                border: 1px solid #444;
                border-radius: 5px;
                color: #fff;
            }}
            .user-info {{
                display: flex;
                align-items: center;
                gap: 10px;
                color: #ccc;
            }}
            .avatar {{
                width: 35px;
                height: 35px;
                background: #00C4B4;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #000;
                font-weight: bold;
            }}
            .container {{
                display: flex;
                min-height: calc(100vh - 63px);
            }}
            .sidebar {{
                width: 220px;
                background: #222;
                padding: 20px 0;
                border-right: 1px solid #333;
            }}
            .sidebar a {{
                display: block;
                padding: 12px 25px;
                color: #ccc;
                text-decoration: none;
                transition: all 0.2s;
            }}
            .sidebar a:hover, .sidebar a.active {{
                background: #00C4B4;
                color: #000;
                font-weight: bold;
            }}
            .main-content {{
                flex: 1;
                padding: 30px;
            }}
            h1 {{
                color: #00C4B4;
                margin-bottom: 20px;
                font-size: 32px;
                display: inline-block;
            }}
            .header-actions {{
                margin-bottom: 30px;
            }}
            .btn-primary {{
                background: #00C4B4;
                color: #000;
                padding: 12px 24px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                text-decoration: none;
                display: inline-block;
                cursor: pointer;
                margin-left: 20px;
            }}
            .btn-primary:hover {{
                background: #00d4c4;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: #222;
                border-radius: 8px;
                overflow: hidden;
            }}
            th {{
                background: #333;
                padding: 15px;
                text-align: left;
                color: #00C4B4;
                font-weight: bold;
                border-bottom: 2px solid #00C4B4;
            }}
            td {{
                padding: 15px;
                border-bottom: 1px solid #333;
                color: #ccc;
            }}
            tr:hover {{
                background: #2a2a2a;
            }}
            .empty-message {{
                text-align: center;
                color: #888;
                padding: 40px;
                font-style: italic;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">Quick Click Repairs</div>
            <div class="search-bar">
                <input type="text" placeholder="Search...">
            </div>
            <div class="user-info">
                <span>Alan ▼</span>
                <div class="avatar">A</div>
            </div>
        </div>
        <div class="container">
            <div class="sidebar">
                <a href="/dashboard">Dashboard</a>
                <a href="/customers" class="active">Customers</a>
                <a href="#">Organizations</a>
                <a href="#">Invoices</a>
                <a href="#">Customer Purchases</a>
                <a href="#">Refurbs</a>
                <a href="#">Tickets</a>
                <a href="#">Parts</a>
                <a href="#">Inventory</a>
                <a href="#">Purchase Orders</a>
                <a href="#">POS</a>
                <a href="#">Reports</a>
                <a href="#">Admin</a>
                <a href="#">Help</a>
                <a href="/logout">Logout</a>
            </div>
            <div class="main-content">
                <div class="header-actions">
                    <h1>Customers</h1>
                    <a href="/customers/new" class="btn-primary">+ New Customer</a>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Business Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Created At</th>
                            <th>Check-in At</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/customers/new", response_class=HTMLResponse)
async def new_customer_form(request: Request, user = Depends(require_auth)):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>New Customer - Quick Click Repairs</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: Arial, sans-serif;
                background: #1a1a1a;
                color: #fff;
            }
            .header {
                background: #222;
                padding: 15px 30px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: 2px solid #00C4B4;
            }
            .logo {
                font-size: 20px;
                font-weight: bold;
                color: #00C4B4;
            }
            .search-bar {
                flex: 1;
                max-width: 500px;
                margin: 0 30px;
            }
            .search-bar input {
                width: 100%;
                padding: 10px 15px;
                background: #333;
                border: 1px solid #444;
                border-radius: 5px;
                color: #fff;
            }
            .user-info {
                display: flex;
                align-items: center;
                gap: 10px;
                color: #ccc;
            }
            .avatar {
                width: 35px;
                height: 35px;
                background: #00C4B4;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #000;
                font-weight: bold;
            }
            .container {
                display: flex;
                min-height: calc(100vh - 63px);
            }
            .sidebar {
                width: 220px;
                background: #222;
                padding: 20px 0;
                border-right: 1px solid #333;
            }
            .sidebar a {
                display: block;
                padding: 12px 25px;
                color: #ccc;
                text-decoration: none;
                transition: all 0.2s;
            }
            .sidebar a:hover, .sidebar a.active {
                background: #00C4B4;
                color: #000;
                font-weight: bold;
            }
            .main-content {
                flex: 1;
                padding: 30px;
                max-width: 800px;
            }
            h1 {
                color: #00C4B4;
                margin-bottom: 30px;
                font-size: 32px;
            }
            .form-card {
                background: #222;
                padding: 30px;
                border-radius: 8px;
                border: 1px solid #333;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                color: #ccc;
                margin-bottom: 8px;
                font-size: 14px;
            }
            label .required {
                color: #ff6b6b;
            }
            input {
                width: 100%;
                padding: 12px;
                background: #333;
                border: 1px solid #444;
                border-radius: 5px;
                color: #fff;
                font-size: 14px;
            }
            input:focus {
                outline: none;
                border-color: #00C4B4;
            }
            .form-actions {
                display: flex;
                gap: 15px;
                margin-top: 30px;
            }
            button {
                padding: 12px 30px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.2s;
            }
            .btn-submit {
                background: #00C4B4;
                color: #000;
            }
            .btn-submit:hover {
                background: #00d4c4;
            }
            .btn-cancel {
                background: #444;
                color: #fff;
            }
            .btn-cancel:hover {
                background: #555;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">Quick Click Repairs</div>
            <div class="search-bar">
                <input type="text" placeholder="Search...">
            </div>
            <div class="user-info">
                <span>Alan ▼</span>
                <div class="avatar">A</div>
            </div>
        </div>
        <div class="container">
            <div class="sidebar">
                <a href="/dashboard">Dashboard</a>
                <a href="/customers" class="active">Customers</a>
                <a href="#">Organizations</a>
                <a href="#">Invoices</a>
                <a href="#">Customer Purchases</a>
                <a href="#">Refurbs</a>
                <a href="#">Tickets</a>
                <a href="#">Parts</a>
                <a href="#">Inventory</a>
                <a href="#">Purchase Orders</a>
                <a href="#">POS</a>
                <a href="#">Reports</a>
                <a href="#">Admin</a>
                <a href="#">Help</a>
                <a href="/logout">Logout</a>
            </div>
            <div class="main-content">
                <h1>New Customer</h1>
                
                <div class="form-card">
                    <form method="post" action="/customers/new">
                        <div class="form-group">
                            <label>First Name <span class="required">*</span></label>
                            <input type="text" name="first_name" required>
                        </div>
                        
                        <div class="form-group">
                            <label>Last Name <span class="required">*</span></label>
                            <input type="text" name="last_name" required>
                        </div>
                        
                        <div class="form-group">
                            <label>Business Name</label>
                            <input type="text" name="business_name">
                        </div>
                        
                        <div class="form-group">
                            <label>Email <span class="required">*</span></label>
                            <input type="email" name="email" required>
                        </div>
                        
                        <div class="form-group">
                            <label>Phone <span class="required">*</span></label>
                            <input type="tel" name="phone" required>
                        </div>
                        
                        <div class="form-actions">
                            <button type="submit" class="btn-submit">Create Customer</button>
                            <button type="button" class="btn-cancel" onclick="window.location.href='/customers'">Cancel</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/customers/new")
async def create_customer(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    business_name: Optional[str] = Form(None),
    email: str = Form(...),
    phone: str = Form(...),
    user = Depends(require_auth),
    db: Session = Depends(get_db)
):
    print(f"[DEBUG] Creating customer: {first_name} {last_name} ({email})")
    
    try:
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            business_name=business_name if business_name else None,
            email=email,
            phone=phone
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        print(f"[DEBUG] Customer created successfully with ID: {customer.id}")
        
        return RedirectResponse(url="/customers", status_code=302)
    except Exception as e:
        print(f"[ERROR] Failed to create customer: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create customer")

@app.post("/customers/{customer_id}/checkin")
async def checkin_customer(
    customer_id: int,
    request: Request,
    user = Depends(require_auth),
    db: Session = Depends(get_db)
):
    print(f"[DEBUG] Checking in customer ID: {customer_id}")
    
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            print(f"[ERROR] Customer {customer_id} not found")
            raise HTTPException(status_code=404, detail="Customer not found")
        
        if customer.check_in_at:
            print(f"[DEBUG] Customer {customer_id} already checked in")
            return RedirectResponse(url="/customers", status_code=302)
        
        customer.check_in_at = datetime.utcnow()
        db.commit()
        print(f"[DEBUG] Customer {customer_id} checked in at {customer.check_in_at}")
        
        return RedirectResponse(url="/customers", status_code=302)
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to check in customer: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to check in customer")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
