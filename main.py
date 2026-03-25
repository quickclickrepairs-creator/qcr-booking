from fastapi import FastAPI, Depends, HTTPException, Response
import pydantic
from typing import List
from datetime import timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json

# Database configuration
DATABASE_URL = "postgresql://user:password@host:port/dbname"
DB_ENGINE = create_engine(DATABASE_URL)

# Initialize the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=DB_ENGINE)
Base = declarative_base()

# Define a custom response type for API routes
class ResponseModel:
    success: bool
    message: str

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    business_name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    customer_email = Column(String, nullable=True)
    device_type = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    fault_type = Column(String, nullable=False)
    faults = Column(Text, nullable=False)
    accessories = Column(String, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    status = Column(String, default="Open")

# Initialize the database session
def get_db():
    # Create a new engine and bind it to the DB connection
    return SessionLocal()

# Define a custom form for user registration (optional)
class UserRegisterForm(pydantic.BaseModel):
    username: str
    email: str
    password: str

# Define a custom form for customer creation (optional)
class CustomerCreateForm(pydantic BaseModel):
    first_name: str
    last_name: str
    business_name: str
    email: str
    phone: str

# Helper functions
def get_db():
    return SessionLocal()

def require_auth(token: str = Depends()):
    # Check if the token is valid and set as an authentication scheme
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token

# Define routes
@app.get("/admin/dashboard", dependencies=[Depends(get_db)], status_code=200)
def get_dashboard():
    try:
        # Get the current user (if any) from the database session
        user = get_db().query(User).first()
        
        if not user:
            return ResponseModel(success=False, message="Unauthorized")
        
        # Create a new list to store customer data
        customers: List[Customer] = []
        for customer in Customer.query.all():
            if customer.customer_id == user.id:
                continue
                
            # Get the customer's current check-in time
            check_in_time = get_db().query(Ticket).filter(Ticket.customer_id == customer.id, Ticket.status == "Open").first()
            
            # Set the check-in time to None (assuming it's a new ticket)
            if check_in_time:
                customers.append(customer)
                
        # Create a new table with recent tickets
        get_db().create_all()
        
        return ResponseModel(success=True, message="Dashboard updated")
    
    except Exception as e:
        print(e)
        return ResponseModel(success=False, message="Error", detail=str(e))

@app.get("/admin/customers",
          dependencies=[Depends(get_db), Depends(require_auth)],
          status_code=200,
          response_model=List[User])
def get_customers():
    try:
        # Get the current user from the database session
        user = get_db().query(User).first()
        
        if not user:
            return ResponseModel(success=False, message="Unauthorized")
        
        # Create a new list to store customer data
        customers: List[Customer] = []
        for customer in Customer.query.all():
            if customer.customer_id == user.id:
                continue
                
            # Get the customer's current check-in time and add it to their profile
            get_db().query(Ticket).filter(Ticket.customer_id == customer.id, Ticket.status == "Open").first()
            customers.append(customer)
        
        return ResponseModel(success=True, message="Customers list updated")
    
    except Exception as e:
        print(e)
        return ResponseModel(success=False, message="Error", detail=str(e))

@app.post("/admin/customers/new",
          dependencies=[Depends(get_db), Depends(require_auth)],
          status_code=200,
          response_model=UserRegisterForm)
def create_customer(customer_register_form: UserRegisterForm):
    try:
        # Create a new customer and send welcome WhatsApp
        new_customer = Customer(first_name=customer_register_form.first_name, last_name=customer_register_form.last_name, business_name=customer_register_form.business_name, email=customer_register_form.email, phone=customer_register_form.phone)
        get_db().add(new_customer)
        
        # Send welcome message to the customer
        send_whatsapp(customer_register_form.email, "Welcome! Our system is excited to have you aboard.")
        
        return ResponseModel(success=True, message="Customer created successfully")
    
    except Exception as e:
        print(e)
        return ResponseModel(success=False, message="Error", detail=str(e))

@app.get("/admin/customers/{customer_id}",
          dependencies=[Depends(get_db), Depends(require_auth)],
          status_code=200,
          response_model=User)
def get_customer(customer_id: int):
    try:
        # Get the customer from the database session
        customer = get_db().query(Customer).filter(Customer.id == customer_id).first()
        
        if not customer:
            return ResponseModel(success=False, message="Customer not found")
        
        return ResponseModel(success=True, message="Customer retrieved successfully", data=customer)
    
    except Exception as e:
        print(e)
        return ResponseModel(success=False, message="Error", detail=str(e))

@app.post("/admin/customers/{customer_id}/new",
          dependencies=[Depends(get_db), Depends(require_auth)],
          status_code=200,
          response_model=UserCreateForm)
def create_customer_new(customer_create_form: CustomerCreateForm):
    try:
        # Create a new customer and send welcome WhatsApp
        new_customer = Customer(first_name=customer_create_form.first_name, last_name=customer_create_form.last_name, business_name=customer_create_form.business_name, email=customer_create_form.email, phone=customer_create_form.phone)
        get_db().add(new_customer)
        
        # Send welcome message to the customer
        send_whatsapp(customer_create_form.email, "Welcome! Our system is excited to have you aboard.")
        
        return ResponseModel(success=True, message="Customer created successfully")
    
    except Exception as e:
        print(e)
        return ResponseModel(success=False, message="Error", detail=str(e))

@app.get("/admin/tickets",
          dependencies=[Depends(get_db), Depends(require_auth)],
          status_code=200,
          response_model=List[Ticket])
def get_tickets():
    try:
        # Get the current user from the database session
        user = get_db().query(User).first()
        
        if not user:
            return ResponseModel(success=False, message="Unauthorized")
        
        # Create a new list to store ticket data
        tickets: List[Ticket] = []
        for ticket in Ticket.query.all():
            if ticket.customer_id == user.id:
                continue
                
            # Get the customer's current check-in time and add it to their profile
            get_db().query(Ticket).filter(Ticket.customer_id == ticket.customer_id, Ticket.status == "Open").first()
            tickets.append(ticket)
        
        return ResponseModel(success=True, message="Tickets list updated", data=tickets)
    
    except Exception as e:
        print(e)
        return ResponseModel(success=False, message="Error", detail=str(e))

@app.post("/admin/tickets/new",
          dependencies=[Depends(get_db), Depends(require_auth)],
          status_code=200,
          response_model=TicketCreateForm)
def create_ticket(ticket_create_form: TicketCreateForm):
    try:
        # Create a new ticket and send WhatsApp notification to the customer
        new_ticket = Ticket(customer_id=get_db().query(Ticket).filter(Ticket.customer_id == get_db().query(User).first().id).first(), 
                              device_type=ticket_create_form.device_type, 
                              brand=ticket_create_form.brand, 
                              model=ticket_create_form.model, 
                              fault_type=ticket_create_form.fault_type, 
                              faults=ticket_create_form.faults, 
                              accessories=ticket_create_form.accessories, 
                              estimated_cost=ticket_create_form.estimated_cost, 
                              status=ticket_create_form.status)
        get_db().add(new_ticket)
        
        # Send welcome message to the customer
        send_whatsapp(ticket_create_form.customer_email, "New ticket! Our system is excited to help you.")
        
        return ResponseModel(success=True, message="Ticket created successfully")
    
    except Exception as e:
        print(e)
        return ResponseModel(success=False, message="Error", detail=str(e))

@app.get("/admin/tickets/{ticket_id}",
          dependencies=[Depends(get_db), Depends(require_auth)],
          status_code=200,
          response_model=Ticket)
def get_ticket(ticket_id: int):
    try:
        # Get the ticket from the database session
        ticket = get_db().query(Ticket).filter(Ticket.id == ticket_id).first()
        
        if not ticket:
            return ResponseModel(success=False, message="Ticket not found")
        
        return ResponseModel(success=True, message="Ticket retrieved successfully", data=ticket)
    
    except Exception as e:
        print(e)
        return ResponseModel(success=False, message="Error", detail=str(e))

@app.post("/admin/tickets/{ticket_id}/new",
          dependencies=[Depends(get_db), Depends(require_auth)],
          status_code=200,
          response_model=TicketCreateForm)
def create_ticket_new(ticket_create_form: TicketCreateForm):
    try:
        # Create a new ticket and send WhatsApp notification to the customer
        new_ticket = Ticket(customer_id=get_db().query(Ticket).filter(Ticket.id == ticket_id).first(), 
                              device_type=ticket_create_form.device_type, 
                              brand=ticket_create_form.brand, 
                              model=ticket_create_form.model, 
                              fault_type=ticket_create_form.fault_type, 
                              faults=ticket_create_form.faults, 
                              accessories=ticket_create_form.accessories, 
                              estimated_cost=ticket_create_form.estimated_cost, 
                              status=ticket_create_form.status)
        get_db().add(new_ticket)
        
        # Send welcome message to the customer
        send_whatsapp(ticket_create_form.customer_email, "New ticket! Our system is excited to help you.")
        
        return ResponseModel(success=True, message="Ticket created successfully")
    
    except Exception as e:
        print(e)
        return ResponseModel(success=False, message="Error", detail=str(e))
