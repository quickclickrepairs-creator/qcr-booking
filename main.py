from fastapi import FastAPI, Response
import uvicorn
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

app = FastAPI()

# Database settings
host = "localhost"
port = 8000
database = f"sqlite:///example.db"

# Create database connection
engine = create_engine(f"F PostgreSQL://{username}:{password}@{host}/{database}", echo=True)
BaseModel.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    return SessionLocal()

class Customer(BaseModel):
    id: int
    first_name: str
    last_name: str
    business_name: str
    email: str
    phone: str

class Ticket(BaseModel):
    id: int
    customer_name: str
    customer_phone: str
    customer_email: str
    device_type: str
    brand: str
    model: str
    fault_type: str
    faults: list[str]
    accessories: list[str]
    estimated_cost: float

class Dashboard(BaseModel):
    title: str
    content: str
    active_menu: str = "Dashboard"

def send_whatsapp(to_phone, message):
    # WhatsApp API settings
    whatsapp_api_key = "YOUR_API_KEY"
    whatsapp_api_secret = "YOUR_API_SECRET"

    # Send WhatsApp notification
    headers = {
        'Authorization': f'Bearer {whatsapp_api_key}',
        'Content-Type': 'application/json'
    }
    data = {'to_phone': to_phone, 'message': message}
    response = requests.post(f'https://api.whatsapp.com/api/{whatsapp_api_key}/send', json=data, headers=headers)
    if response.status_code == 200:
        print("WhatsApp notification sent successfully")

def get_page_layout(title: str, content: str, active_menu: str = "") -> str:
    html = f"""
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #000;
            }
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <p>{content}</p>
        {active_menu}
        <form action="/admin/tickets/new">
            <label for="device_type">Device Type:</label>
            <select id="device_type" name="device_type">
                <option value="">Select</option>
                <option value="Desktop">Desktop</option>
                <option value="Tablet">Tablet</option>
                <option value="Mobile">Mobile</option>
            </select><br><label for="fault_type">Fault Type:</label>
            <select id="fault_type" name="fault_type">
                <option value="">Select</option>
                <option value="Electrical">Electrical</option>
                <option value="Circuit Breaker">Circuit Breaker</option>
                <option value="Other">Other</option>
            </select><br><button type="submit">New Ticket</button>
        </form>
    </body>
    </html>
    """
    return html

# Define routes
# New comprehensive routes for dashboard, customers, and tickets.

@app.get("/admin/dashboard")
async def admin_dashboard():
    # Logic to render dashboard
    return templates.TemplateResponse("dashboard.html", context={})

@app.get("/admin/customers")
async def admin_customers():
    # Logic to fetch customers
    customers = fetch_customers_from_db()
    return templates.TemplateResponse("customers.html", context={"customers": customers})

@app.get("/admin/tickets")
async def admin_tickets():
    # Logic to fetch tickets
    tickets = fetch_tickets_from_db()
    return templates.TemplateResponse("tickets.html", context={"tickets": tickets})

@app.post("/admin/tickets/")
async def create_ticket(ticket_data: TicketCreate):
    # Logic to create a new ticket in the database
    create_ticket_in_db(ticket_data)
    return RedirectResponse(url="/admin/tickets", status_code=303)
