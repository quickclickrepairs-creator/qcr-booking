import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Request, Form, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from twilio.rest import Client

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/repairshop")
print(f"[DEBUG] Connecting to database: {DATABASE_URL[:20]}...")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Twilio setup
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
YOUR_WHATSAPP_NUMBER = os.getenv("YOUR_WHATSAPP_NUMBER", "whatsapp:+447863743275")

def send_whatsapp_message(to_phone: str, message: str):
    """Send WhatsApp message via Twilio"""
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        print("[WARNING] Twilio credentials not configured, skipping WhatsApp message")
        return False
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        # Ensure phone number has whatsapp: prefix
        if not to_phone.startswith("whatsapp:"):
            to_phone = f"whatsapp:{to_phone}"
        
        message = client.messages.create(
            from_=YOUR_WHATSAPP_NUMBER,
            body=message,
            to=to_phone
        )
        print(f"[DEBUG] WhatsApp message sent successfully: {message.sid}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send WhatsApp message: {e}")
        return False

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

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    customer_email = Column(String, nullable=True)
    device_type = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    faults = Column(Text, nullable=False)
    accessories = Column(String, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    status = Column(String, default="Open")
    created_at = Column(DateTime, default=datetime.utcnow)

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
    if not session_id or session_id not in sessions:
        return None
    return sessions[session_id]

def require_auth(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user

# Helper function for common layout
def get_page_layout(title: str, content: str, active_menu: str = ""):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title} - Quick Click Repairs</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
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
                margin-bottom: 30px;
                font-size: 32px;
            }}
            .coming-soon {{
                text-align: center;
                padding: 60px;
                color: #888;
                font-size: 24px;
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
                <a href="/dashboard" class="{'active' if active_menu == 'dashboard' else ''}">Dashboard</a>
                <a href="/customers" class="{'active' if active_menu == 'customers' else ''}">Customers</a>
                <a href="/organizations" class="{'active' if active_menu == 'organizations' else ''}">Organizations</a>
                <a href="/invoices" class="{'active' if active_menu == 'invoices' else ''}">Invoices</a>
                <a href="/purchases" class="{'active' if active_menu == 'purchases' else ''}">Customer Purchases</a>
                <a href="/refurbs" class="{'active' if active_menu == 'refurbs' else ''}">Refurbs</a>
                <a href="/tickets" class="{'active' if active_menu == 'tickets' else ''}">Tickets</a>
                <a href="/parts" class="{'active' if active_menu == 'parts' else ''}">Parts</a>
                <a href="/inventory" class="{'active' if active_menu == 'inventory' else ''}">Inventory</a>
                <a href="/purchase-orders" class="{'active' if active_menu == 'purchase-orders' else ''}">Purchase Orders</a>
                <a href="/pos" class="{'active' if active_menu == 'pos' else ''}">POS</a>
                <a href="/reports" class="{'active' if active_menu == 'reports' else ''}">Reports</a>
                <a href="/admin" class="{'active' if active_menu == 'admin' else ''}">Admin</a>
                <a href="/help" class="{'active' if active_menu == 'help' else ''}">Help</a>
                <a href="/logout">Logout</a>
            </div>
            <div class="main-content">
                {content}
            </div>
        </div>
    </body>
    </html>
    """

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
    
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="session_id")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user = Depends(require_auth)):
    content = """
    <style>
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
            margin-bottom: 30px;
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
        .charts-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 40px;
        }
        .chart-container {
            background: #222;
            padding: 25px;
            border-radius: 8px;
            border: 1px solid #333;
        }
        canvas {
            max-height: 300px;
        }
    </style>
    
    <h1>Welcome!</h1>
    
    <h2>Get Started</h2>
    <div class="get-started">
        <a href="/customers/new" class="action-btn">+ New Customer</a>
        <a href="/tickets/new" class="action-btn">+ New Ticket</a>
        <a href="/checkin" class="action-btn">+ New Check In</a>
        <a href="/invoices/new" class="action-btn">+ New Invoice</a>
        <a href="/estimates/new" class="action-btn">+ New Estimate</a>
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
    
    <h2>Analytics</h2>
    <div class="charts-row">
        <div class="chart-container">
            <h3>Tickets Per Day (Last 7 Days)</h3>
            <canvas id="ticketsChart"></canvas>
        </div>
        <div class="chart-container">
            <h3>Payments by Hour of Day</h3>
            <canvas id="paymentsChart"></canvas>
        </div>
    </div>
    
    <script>
        // Tickets per day chart
        const ticketsCtx = document.getElementById('ticketsChart').getContext('2d');
        new Chart(ticketsCtx, {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Tickets',
                    data: [12, 19, 8, 15, 22, 18, 10],
                    backgroundColor: '#00C4B4',
                    borderColor: '#00C4B4',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        labels: {
                            color: '#ccc'
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: '#ccc'
                        },
                        grid: {
                            color: '#333'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#ccc'
                        },
                        grid: {
                            color: '#333'
                        }
                    }
                }
            }
        });
        
        // Payments by hour chart
        const paymentsCtx = document.getElementById('paymentsChart').getContext('2d');
        new Chart(paymentsCtx, {
            type: 'bar',
            data: {
                labels: ['9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM'],
                datasets: [{
                    label: 'Payments (£)',
                    data: [120, 250, 180, 320, 290, 210, 380, 150, 90],
                    backgroundColor: '#00C4B4',
                    borderColor: '#00C4B4',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        labels: {
                            color: '#ccc'
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: '#ccc',
                            callback: function(value) {
                                return '£' + value;
                            }
                        },
                        grid: {
                            color: '#333'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#ccc'
                        },
                        grid: {
                            color: '#333'
                        }
                    }
                }
            }
        });
    </script>
    """
    
    return HTMLResponse(content=get_page_layout("Dashboard", content, "dashboard"))

# Placeholder pages
@app.get("/organizations", response_class=HTMLResponse)
async def organizations(request: Request, user = Depends(require_auth)):
    content = '<div class="coming-soon">🏢 Organizations - Coming Soon</div>'
    return HTMLResponse(content=get_page_layout("Organizations", content, "organizations"))

@app.get("/invoices", response_class=HTMLResponse)
async def invoices(request: Request, user = Depends(require_auth)):
    content = '<div class="coming-soon">📄 Invoices - Coming Soon</div>'
    return HTMLResponse(content=get_page_layout("Invoices", content, "invoices"))

@app.get("/invoices/new", response_class=HTMLResponse)
async def new_invoice(request: Request, user = Depends(require_auth)):
    content = '<div class="coming-soon">📝 New Invoice - Coming Soon</div>'
    return HTMLResponse(content=get_page_layout("New Invoice", content, "invoices"))

@app.get("/purchases", response_class=HTMLResponse)
async def purchases(request: Request, user = Depends(require_auth)):
    content = '<div class="coming-soon">🛒 Customer Purchases - Coming Soon</div>'
    return HTMLResponse(content=get_page_layout("Customer Purchases", content, "purchases"))

@app.get("/refurbs", response_class=HTMLResponse)
async def refurbs(request: Request, user = Depends(require_auth)):
    content = '<div class="coming-soon">🔧 Refurbs - Coming Soon</div>'
    return HTMLResponse(content=get_page_layout("Refurbs", content, "refurbs"))

@app.get("/parts", response_class=HTMLResponse)
async def parts(request: Request, user = Depends(require_auth)):
    content = '<div class="coming-soon">⚙️ Parts - Coming Soon</div>'
    return HTMLResponse(content=get_page_layout("Parts", content, "parts"))

@app.get("/inventory", response_class=HTMLResponse)
async def inventory(request: Request, user = Depends(require_auth)):
    content = '<div class="coming-soon">📦 Inventory - Coming Soon</div>'
    return HTMLResponse(content=get_page_layout("Inventory", content, "inventory"))

@app.get("/purchase-orders", response_class=HTMLResponse)
async def purchase_orders(request: Request, user = Depends(require_auth)):
    content = '<div class="coming-soon">📋 Purchase Orders - Coming Soon</div>'
    return HTMLResponse(content=get_page_layout("Purchase Orders", content, "purchase-orders"))

@app.get("/pos", response_class=HTMLResponse)
async def pos(request: Request, user = Depends(require_auth)):
    content = '<div class="coming-soon">💳 POS - Coming Soon</div>'
    return HTMLResponse(content=get_page_layout("POS", content, "pos"))

@app.get("/reports", response_class=HTMLResponse)
async def reports(request: Request, user = Depends(require_auth)):
    content = '<div class="coming-soon">📊 Reports - Coming Soon</div>'
    return HTMLResponse(content=get_page_layout("Reports", content, "reports"))

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request, user = Depends(require_auth)):
    content = '<div class="coming-soon">⚙️ Admin - Coming Soon</div>'
    return HTMLResponse(content=get_page_layout("Admin", content, "admin"))

@app.get("/help", response_class=HTMLResponse)
async def help_page(request: Request, user = Depends(require_auth)):
    content = '<div class="coming-soon">❓ Help - Coming Soon</div>'
    return HTMLResponse(content=get_page_layout("Help", content, "help"))

@app.get("/checkin", response_class=HTMLResponse)
async def checkin(request: Request, user = Depends(require_auth)):
    content = '<div class="coming-soon">✅ New Check In - Coming Soon</div>'
    return HTMLResponse(content=get_page_layout("New Check In", content, ""))

@app.get("/estimates/new", response_class=HTMLResponse)
async def new_estimate(request: Request, user = Depends(require_auth)):
    content = '<div class="coming-soon">💰 New Estimate - Coming Soon</div>'
    return HTMLResponse(content=get_page_layout("New Estimate", content, ""))

# Customer routes
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
        rows_html = '<tr><td colspan="8" style="text-align:center;color:#888;padding:40px;font-style:italic;">No customers yet. Add your first customer!</td></tr>'
    
    content = f"""
    <style>
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
    </style>
    
    <div class="header-actions">
        <h1 style="display:inline-block;">Customers</h1>
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
    """
    
    return HTMLResponse(content=get_page_layout("Customers", content, "customers"))

@app.get("/customers/new", response_class=HTMLResponse)
async def new_customer_form(request: Request, user = Depends(require_auth)):
    content = """
    <style>
        .form-card {
            background: #222;
            padding: 30px;
            border-radius: 8px;
            border: 1px solid #333;
            max-width: 600px;
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
                <input type="tel" name="phone" required placeholder="+44...">
            </div>
            
            <div class="form-actions">
                <button type="submit" class="btn-submit">Create Customer</button>
                <button type="button" class="btn-cancel" onclick="window.location.href='/customers'">Cancel</button>
            </div>
        </form>
    </div>
    """
    
    return HTMLResponse(content=get_page_layout("New Customer", content, "customers"))

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
        
        # Send WhatsApp notification
        message = f"Welcome to Quick Click Repairs, {first_name}! We've added you to our system. Call us at 023 8036 1277 for any assistance."
        send_whatsapp_message(phone, message)
        
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
            raise HTTPException(status_code=404, detail="Customer not found")
        
        if customer.check_in_at:
            return RedirectResponse(url="/customers", status_code=302)
        
        customer.check_in_at = datetime.utcnow()
        db.commit()
        print(f"[DEBUG] Customer {customer_id} checked in at {customer.check_in_at}")
        
        # Send WhatsApp notification
        message = f"Hi {customer.first_name}, you've been checked in at Quick Click Repairs. We'll attend to you shortly!"
        send_whatsapp_message(customer.phone, message)
        
        return RedirectResponse(url="/customers", status_code=302)
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to check in customer: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to check in customer")

# Ticket routes
@app.get("/tickets", response_class=HTMLResponse)
async def tickets_list(request: Request, user = Depends(require_auth), db: Session = Depends(get_db)):
    try:
        tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).all()
        print(f"[DEBUG] Fetched {len(tickets)} tickets from database")
    except Exception as e:
        print(f"[ERROR] Failed to fetch tickets: {e}")
        tickets = []
    
    rows_html = ""
    if tickets:
        for ticket in tickets:
            status_color = "#00C4B4" if ticket.status == "Open" else "#888"
            rows_html += f"""
            <tr>
                <td>{ticket.id}</td>
                <td>{ticket.customer_name}</td>
                <td>{ticket.device_type}</td>
                <td>{ticket.brand} {ticket.model}</td>
                <td>{ticket.faults[:50]}...</td>
                <td style="color:{status_color};font-weight:bold;">{ticket.status}</td>
                <td>{ticket.created_at.strftime("%Y-%m-%d %H:%M")}</td>
            </tr>
            """
    else:
        rows_html = '<tr><td colspan="7" style="text-align:center;color:#888;padding:40px;font-style:italic;">No tickets yet. Create your first ticket!</td></tr>'
    
    content = f"""
    <style>
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
    </style>
    
    <div class="header-actions">
        <h1 style="display:inline-block;">Tickets</h1>
        <a href="/tickets/new" class="btn-primary">+ New Ticket</a>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Customer</th>
                <th>Device Type</th>
                <th>Brand/Model</th>
                <th>Faults</th>
                <th>Status</th>
                <th>Created</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """
    
    return HTMLResponse(content=get_page_layout("Tickets", content, "tickets"))

@app.get("/tickets/new", response_class=HTMLResponse)
async def new_ticket_form(request: Request, user = Depends(require_auth)):
    content = """
    <style>
        .form-card {
            background: #222;
            padding: 30px;
            border-radius: 8px;
            border: 1px solid #333;
            max-width: 800px;
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
        input, textarea, select {
            width: 100%;
            padding: 12px;
            background: #333;
            border: 1px solid #444;
            border-radius: 5px;
            color: #fff;
            font-size: 14px;
        }
        textarea {
            min-height: 100px;
            resize: vertical;
        }
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #00C4B4;
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
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
    
    <h1>New Ticket</h1>
    
    <div class="form-card">
        <form method="post" action="/tickets/new">
            <h3 style="color:#00C4B4;margin-bottom:20px;">Customer Details</h3>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Customer Name <span class="required">*</span></label>
                    <input type="text" name="customer_name" required>
                </div>
                
                <div class="form-group">
                    <label>Customer Phone <span class="required">*</span></label>
                    <input type="tel" name="customer_phone" required placeholder="+44...">
                </div>
            </div>
            
            <div class="form-group">
                <label>Customer Email</label>
                <input type="email" name="customer_email">
            </div>
            
            <h3 style="color:#00C4B4;margin:30px 0 20px 0;">Device Details</h3>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Device Type <span class="required">*</span></label>
                    <select name="device_type" required>
                        <option value="">Select device type</option>
                        <option value="Phone">Phone</option>
                        <option value="Tablet">Tablet</option>
                        <option value="Laptop">Laptop</option>
                        <option value="Desktop">Desktop</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Brand <span class="required">*</span></label>
                    <input type="text" name="brand" required placeholder="e.g. Apple, Samsung">
                </div>
            </div>
            
            <div class="form-group">
                <label>Model <span class="required">*</span></label>
                <input type="text" name="model" required placeholder="e.g. iPhone 13, Galaxy S21">
            </div>
            
            <div class="form-group">
                <label>Faults/Issues <span class="required">*</span></label>
                <textarea name="faults" required placeholder="Describe the problem..."></textarea>
            </div>
            
            <div class="form-group">
                <label>Accessories</label>
                <input type="text" name="accessories" placeholder="e.g. Charger, Case, SIM card">
            </div>
            
            <div class="form-group">
                <label>Estimated Cost (£)</label>
                <input type="number" name="estimated_cost" step="0.01" placeholder="0.00">
            </div>
            
            <div class="form-actions">
                <button type="submit" class="btn-submit">Create Ticket</button>
                <button type="button" class="btn-cancel" onclick="window.location.href='/tickets'">Cancel</button>
            </div>
        </form>
    </div>
    """
    
    return HTMLResponse(content=get_page_layout("New Ticket", content, "tickets"))

@app.post("/tickets/new")
async def create_ticket(
    request: Request,
    customer_name: str = Form(...),
    customer_phone: str = Form(...),
    customer_email: Optional[str] = Form(None),
    device_type: str = Form(...),
    brand: str = Form(...),
    model: str = Form(...),
    faults: str = Form(...),
    accessories: Optional[str] = Form(None),
    estimated_cost: Optional[float] = Form(None),
    user = Depends(require_auth),
    db: Session = Depends(get_db)
):
    print(f"[DEBUG] Creating ticket for: {customer_name} - {device_type}")
    
    try:
        ticket = Ticket(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            device_type=device_type,
            brand=brand,
            model=model,
            faults=faults,
            accessories=accessories,
            estimated_cost=estimated_cost
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        print(f"[DEBUG] Ticket created successfully with ID: {ticket.id}")
        
        # Send WhatsApp notification
        cost_text = f" Estimated cost: £{estimated_cost:.2f}." if estimated_cost else ""
        message = f"Hi {customer_name}, your repair ticket #{ticket.id} has been created for {brand} {model}.{cost_text} We'll update you soon! - Quick Click Repairs"
        send_whatsapp_message(customer_phone, message)
        
        return RedirectResponse(url="/tickets", status_code=302)
    except Exception as e:
        print(f"[ERROR] Failed to create ticket: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create ticket")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
