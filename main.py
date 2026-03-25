from fastapi import FastAPI, Depends, HTTPException, Response, status
import json
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine
from typing import List

app = FastAPI()

# Database connection string
SQLALCHEMY_DATABASE_URL = "sqlite:///quick_click_repair.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Helper function to get the full dark-themed HTML with sidebar and header
def get_page_layout(title: str, content: str, active_menu: str):
    return """
    <div class="container">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <button class="burger" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"> 
                <span class="navbar-brand">Quick Click Repairs</span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item active">
                        <a class="nav-link" href="/dashboard">Dashboard</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/customers">Customers</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/tickets">Tickets</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/check-in">Quick Check-in</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/logout">Logout</a>
                    </li>
                </ul>
            </div>
        </nav>
    </div>
    """

# Helper function to wrap the admin page with dark theme and sidebar
def get_admin_page(title: str, content: str):
    return "<html><head><title>{}</title></head><body style='margin: 0; padding: 0; font-family: Arial, sans-serif;'>".format(title)
    return """
        <div class="container">
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                <button class="burger" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"> 
                    <span class="navbar-brand">{}</span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav ml-auto">
                        <li class="nav-item active">
                            <a class="nav-link" href="/dashboard">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/customers">Customers</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/tickets">Tickets</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/check-in">Quick Check-in</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/logout">Logout</a>
                        </li>
                    </ul>
                </div>
            </nav>
        </div>
    """.format(title)
app.get("/dashboard", get_page_layout("Quick Click Repairs Dashboard", "<h1>Welcome to the Quick Click Repairs dashboard!</h1><p>This is your dashboard for managing customers, tickets, and check-ins.</p>", "Dashboard"))

# Dashboard Route
@app.get("/admin/dashboard")
def read_dashboard():
    return get_page_layout("Quick Click Repairs Dashboard", "<h1>Welcome to the Quick Click Repairs dashboard!</h1><p>This is your dashboard for managing customers, tickets, and check-ins.</p>", "")

# Customers Section
@app.get("/admin/customers")
def read_customers():
    db = get_db()
    # Fetch all customers
    customers = db.query(Customer).all()
    return get_page_layout("Quick Click Repairs Customers", "<h1>Manage your customers here!</h1><table border='1'>", "Customers")

# Tickets Section
@app.get("/admin/tickets")
def read_tickets():
    db = get_db()
    # Fetch all tickets
    tickets = db.query(Ticket).all()
    return get_page_layout("Quick Click Repairs Tickets", "<h1>Manage your tickets here!</h1><table border='1'>", "Tickets")

# New Customer Route
@app.post("/admin/customers/new")
def create_customer(customer_data: Customer):
    db = get_db()
    # Create a new customer
    new_customer = db.query(Customer).filter(Customer.first_name == customer_data.first_name and Customer.last_name == customer_data.last_name).first()
    if not new_customer:
        new_customer = Customer(first_name=customer_data.first_name, last_name=customer_data.last_name)
        db.add(new_customer)
        db.commit()
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

# New Ticket Route
@app.post("/admin/tickets/new")
def create_ticket(ticket_data: Ticket):
    db = get_db()
    # Create a new ticket
    new_ticket = Ticket(customer_id=customer_data["id"], 
                         device_type=ticket_data.device_type, 
                         brand=ticket_data.brand, 
                         model=ticket_data.model, 
                         faults=ticket_data.faults, 
                         accessories=ticket_data.accessories)
    db.add(new_ticket)
    db.commit()
    return Response(status_code=status.HTTP_201_CREATED)

# Ticket Details Route
@app.get("/admin/tickets/{ticket_id}")
def read_ticket(ticket_id: int):
    db = get_db()
    # Fetch the ticket details
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return get_page_layout("Quick Click Repairs Tickets", "<h1>Manage your tickets here!</h1><table border='1'>", "Tickets")

# New Ticket Form
@app.post("/admin/tickets/new")
def create_ticket_form(ticket_data: TicketCreateForm):
    db = get_db()
    # Create a new ticket form
    return Response(status_code=status.HTTP_201_CREATED)
