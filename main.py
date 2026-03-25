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
@app.get("/admin/dashboard")
async def read_root():
    return Dashboard(title="Dashboard", content=f"Welcome to the dashboard!", active_menu="dashboard")

@app.get("/admin/customers/")
async def read_customers():
    db = get_db()
    customers = db.query(Customer).all()
    return [Customer.to_dict() for customer in customers]

@app.post("/admin/customers/new")
async def create_customer(customer: Customer):
    db = get_db()
    new_customer = db.insert(Customer)
    db.commit()
    send_whatsapp(customer.phone, f"Welcome to the system! We will contact you within {timedelta(days=1)} days.")
    return {"message": "Customer created successfully", "customer_id": new_customer}

@app.get("/admin/tickets/")
async def read_tickets():
    db = get_db()
    tickets = db.query(Ticket).all()
    html = get_page_layout("Tickets", f"Here are your tickets:\n\n{', '.join([str(ticket) for ticket in tickets])}")
    return html

@app.post("/admin/tickets/new")
async def create_ticket(ticket: Ticket):
    db = get_db()
    new_ticket = db.insert(Ticket)
    db.commit()
    send_whatsapp(ticket.customer_phone, f"Ticket created successfully! We will contact you within {timedelta(days=1)} days.")
    return {"message": "Ticket created successfully", "ticket_id": new_ticket}

@app.post("/admin/tickets/")
async def delete_ticket():
    db = get_db()
    db.execute("DELETE FROM tickets WHERE id = 1")
    db.commit()
    send_whatsapp("", f"Ticket deleted successfully!")
    return {"message": "Ticket deleted successfully"}
