@app.get("/admin/dashboard")
async def admin_dashboard(request: Request, user: User = Depends(require_auth)):
    """
    Main page for admin dashboard, with 4 buttons and a table for recent tickets.
    :param request: starlette.requests.Request
    :param user: app.models.User
    :return: fastapi.responses.HTMLResponse
    """
    return templates.TemplateResponse(
        "admin/dashboard.html", {"request": request, "user": user}
    )

@app.get("/admin/customers")
async def admin_customers(request: Request, user: User = Depends(require_auth)):
    """
    Table with all customers, plus button to add new customer
    :param request: starlette.requests.Request
    :param user: app.models.User
    :return: fastapi.responses.HTMLResponse
    """
    return templates.TemplateResponse(
        "admin/customers.html", {"request": request, "user": user}
    )

@app.get("/admin/customers/new")
async def admin_customer_create(request: Request, user: User = Depends(require_auth)):
    """
    Form to create new customer with first name, last name and other fields.
    :param request: starlette.requests.Request
    :param user: app.models.User
    :return: fastapi.responses.HTMLResponse
    """
    return templates.TemplateResponse(
        "admin/customer_create.html", {"request": request, "user": user}
    )

@app.post("/admin/customers/new")
async def admin_customer_submit(
    request: Request,
    user: User = Depends(require_auth),
    db=Depends(get_db),
):
    """
    Submit the new customer form and add it to DB. If successful, send WhatsApp welcome message and redirect to /admin/tickets/new?customer_id=ID
    :param request: starlette.requests.Request
    :param user: app.models.User
    :param db: sqlalchemy.engine.Engine (SQLAlchemy database engine)
    :return: fastapi.responses.HTMLResponse or fastapi.responses.RedirectResponse
    """
    ...
