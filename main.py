from fastapi import FastAPI, Depends, HTTPException, Response, status
import json
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine
from typing import List

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///quick_click_repair.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Helper function to get the full dark-themed HTML with sidebar and header
def get_page_layout(title: str, content: str, active_menu: str):
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
