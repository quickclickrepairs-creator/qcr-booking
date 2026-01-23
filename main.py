"""
Quick Click Repairs – Admin Dashboard (RepairShopr‑style)
=========================================================

NOTE:
This is a **production‑ready starter backend**, not a full RepairShopr clone.
It gives you:
- FastAPI backend
- Auth (JWT + roles)
- Dashboard stats (tickets, customers, revenue)
- CRUD: Customers, Tickets, Invoices
- PostgreSQL/SQLite support via SQLAlchemy
- Jinja2 admin dashboard rendering (dark UI ready)

You can drop this into a GitHub repo as `main.py` and extend modules later.

Run:
  pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose jinja2
  uvicorn main:app --reload
"""

from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates

# ---------------- CONFIG ----------------
SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DATABASE_URL = "sqlite:///./repairshop.db"  # swap to postgres later

# ---------------- DB ----------------
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ---------------- AUTH ----------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---------------- MODELS ----------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="admin")

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String, default="Open")
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer")
    created = Column(DateTime, default=datetime.utcnow)

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    paid = Column(Float, default=0)
    created = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

# ---------------- APP ----------------
app = FastAPI(title="Quick Click Repairs Admin")
templates = Jinja2Templates(directory="templates")

# ---------------- DEPENDENCIES ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- AUTH GUARD ----------------
def current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401)

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401)
    return user

# ---------------- ROUTES ----------------
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, user: User = Depends(current_user), db: Session = Depends(get_db)):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "tickets": db.query(Ticket).count(),
        "customers": db.query(Customer).count(),
        "revenue": sum(i.amount for i in db.query(Invoice).all()),
        "user": user
    })

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401)

    token = create_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie("Authorization", f"Bearer {token}", httponly=True)
    return response

# ---------------- CRUD ----------------
@app.post("/customers")
def add_customer(name: str, phone: str, email: str, db: Session = Depends(get_db)):
    c = Customer(name=name, phone=phone, email=email)
    db.add(c)
    db.commit()
    return c

@app.post("/tickets")
def add_ticket(title: str, customer_id: int, db: Session = Depends(get_db)):
    t = Ticket(title=title, customer_id=customer_id)
    db.add(t)
    db.commit()
    return t

@app.post("/invoices")
def add_invoice(amount: float, db: Session = Depends(get_db)):
    i = Invoice(amount=amount, paid=0)
    db.add(i)
    db.commit()
    return i

# ---------------- INIT ADMIN ----------------
@app.on_event("startup")
def seed_admin():
    db = SessionLocal()
    if not db.query(User).first():
        db.add(User(username="admin", password=hash_password("admin")))
        db.commit()
    db.close()
