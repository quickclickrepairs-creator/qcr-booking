CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    business_name VARCHAR(150),
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    check_in_at TIMESTAMP
);
@app.get("/admin/customers")
async def customers_list():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, first_name, last_name, business_name, email, phone, created_at, check_in_at 
                FROM customers 
                ORDER BY created_at DESC
            """))
            customers = result.fetchall()
    except Exception as e:
        print(f"Error loading customers: {str(e)}")
        customers = []

    rows = ""
    for c in customers:
        check_in = c.check_in_at.strftime("%Y-%m-%d %H:%M") if c.check_in_at else "Not checked in"
        rows += f"""
        <tr>
            <td>{c.id}</td>
            <td>{c.first_name} {c.last_name}</td>
            <td>{c.business_name or '-'}</td>
            <td>{c.email}</td>
            <td>{c.phone}</td>
            <td>{c.created_at.strftime("%Y-%m-%d %H:%M")}</td>
            <td>{check_in}</td>
            <td>
                {'<button disabled>Checked In</button>' if c.check_in_at else f'<a href="/admin/checkin/{c.id}" style="background:#00C4B4;color:white;padding:8px 16px;border-radius:6px;text-decoration:none">Check-in Now</a>'}
            </td>
        </tr>
        """

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Customers - Quick Click Repairs</title>
      <style>
        body {{font-family:Arial,sans-serif;background:#1e1e1e;color:#e0e0e0;margin:0;padding:20px}}
        .container {{max-width:1400px;margin:auto}}
        h1 {{color:#00C4B4;text-align:center}}
        table {{width:100%;border-collapse:collapse;background:#2a2a2a;margin-top:20px}}
        th {{background:#00C4B4;color:black;padding:12px;text-align:left}}
        td {{padding:12px;border-bottom:1px solid #444}}
        tr:hover {{background:#333}}
        a.btn {{background:#00C4B4;color:white;padding:12px 24px;border:none;border-radius:8px;text-decoration:none;display:inline-block;margin:20px 0}}
        a.btn:hover {{background:#00a89a}}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Customers</h1>
        <a href="/admin/new-customer" class="btn">+ Add New Customer</a>
        <table>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Business</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Created</th>
            <th>Check-in Time</th>
            <th>Action</th>
          </tr>
          {rows or '<tr><td colspan="8" style="text-align:center">No customers yet</td></tr>'}
        </table>
        <p style="text-align:center;margin-top:40px">
          <a href="/admin/dashboard" style="color:#00C4B4">← Back to Dashboard</a>
        </p>
      </div>
    </body>
    </html>
    """)
    @app.get("/admin/new-customer")
async def new_customer():
    return HTMLResponse("""
    <html>
    <head>
      <title>New Customer</title>
      <style>
        body {font-family:Arial,sans-serif;background:#1e1e1e;color:#e0e0e0;margin:0;padding:40px}
        .container {max-width:600px;margin:auto;background:#2a2a2a;padding:40px;border-radius:15px}
        h1 {color:#00C4B4;text-align:center}
        input {width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white;border:1px solid #444}
        button {background:#00C4B4;color:white;padding:18px;font-size:20px;border:none;border-radius:10px;width:100%;cursor:pointer}
        button:hover {background:#00a89a}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>New Customer</h1>
        <form action="/admin/create-customer" method="post">
          <input name="first_name" placeholder="First Name" required>
          <input name="last_name" placeholder="Last Name" required>
          <input name="business_name" placeholder="Business Name (optional)">
          <input name="email" type="email" placeholder="Email" required>
          <input name="phone" placeholder="Phone Number" required>
          <button type="submit">Save Customer</button>
        </form>
        <p style="text-align:center;margin-top:30px"><a href="/admin/customers" style="color:#00C4B4">← Back to Customers</a></p>
      </div>
    </body>
    </html>
    """)
    @app.post("/admin/create-customer")
async def create_customer(
    first_name: str = Form(...),
    last_name: str = Form(...),
    business_name: str = Form(None),
    email: str = Form(...),
    phone: str = Form(...)
):
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO customers (first_name, last_name, business_name, email, phone)
                VALUES (:first, :last, :business, :email, :phone)
            """), {
                "first": first_name,
                "last": last_name,
                "business": business_name,
                "email": email,
                "phone": phone
            })
            conn.commit()
    except Exception as e:
        return HTMLResponse(f"<h2 style='color:red'>Error: {str(e)}</h2><a href='/admin/new-customer'>← Try again</a>")

    return RedirectResponse("/admin/customers", status_code=303)
    @app.get("/admin/checkin/{customer_id}")
async def checkin_customer(customer_id: int):
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                UPDATE customers 
                SET check_in_at = CURRENT_TIMESTAMP 
                WHERE id = :id AND check_in_at IS NULL
            """), {"id": customer_id})
            conn.commit()
    except Exception as e:
        print(f"Check-in error: {str(e)}")

    return RedirectResponse("/admin/customers", status_code=303)
