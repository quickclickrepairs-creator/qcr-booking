# Public page - disabled message
@app.get("/")
async def public_page():
    return HTMLResponse("""
    <html>
    <head><title>Quick Click Repairs</title></head>
    <body style="font-family:Arial;background:#1e1e1e;color:#e0e0e0;text-align:center;padding:100px">
      <h1 style="color:#00C4B4">Online Booking Disabled</h1>
      <p style="font-size:22px">All bookings are now in-store only.</p>
      <p style="font-size:20px">Please visit the shop or call 023 8036 1277 to schedule.</p>
      <p style="margin-top:60px">
        <a href="/admin" style="color:#00C4B4;font-size:20px">Staff Login →</a>
      </p>
    </body>
    </html>
    """)

# Staff booking form (login required)
@app.get("/admin/new-booking")
async def staff_booking():
    return HTMLResponse("""
    <html>
    <head><title>New Booking - Staff</title></head>
    <body style="font-family:Arial;background:#1e1e1e;color:#e0e0e0;padding:40px">
      <div style="max-width:700px;margin:auto;background:#2a2a2a;padding:40px;border-radius:15px">
        <h1 style="color:#00C4B4;text-align:center">New Booking (Staff Only)</h1>
        <form action="/admin/create-booking" method="post">
          <input name="customer_name" placeholder="Customer Name" required style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
          <input name="customer_phone" placeholder="Phone" required style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
          <select name="service_type" required style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
            <option value="">Service Type</option>
            <option>Laptop Repair</option>
            <option>Phone Repair</option>
            <option>Other</option>
          </select>
          <input name="appointment_date" type="date" required style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
          <input name="appointment_time" type="time" required style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
          <textarea name="description" rows="4" placeholder="Notes" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white"></textarea>
          <button type="submit" style="background:#00C4B4;color:white;padding:18px;font-size:20px;border:none;border-radius:10px;width:100%;cursor:pointer">Create Booking</button>
        </form>
        <p style="text-align:center;margin-top:30px"><a href="/admin" style="color:#00C4B4">← Back to Dashboard</a></p>
      </div>
    </body>
    </html>
    """)

@app.post("/admin/create-booking")
async def create_booking(
    customer_name: str = Form(...),
    customer_phone: str = Form(...),
    service_type: str = Form(...),
    appointment_date: str = Form(...),
    appointment_time: str = Form(...),
    description: str = Form("")
):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO bookings (customer_name, customer_phone, service_type, appointment_date, appointment_time, description)
            VALUES (:name, :phone, :service, :date, :time, :desc)
        """), {
            "name": customer_name,
            "phone": customer_phone,
            "service": service_type,
            "date": appointment_date,
            "time": appointment_time,
            "desc": description
        })
        conn.commit()

    return HTMLResponse("""
    <html>
    <body style="font-family:Arial;background:#1e1e1e;color:#e0e0e0;text-align:center;padding:100px">
      <h1 style="color:#00C4B4">Booking Created!</h1>
      <p style="font-size:22px">Booking for {customer_name} saved successfully.</p>
      <p style="margin-top:40px">
        <a href="/admin" style="color:#00C4B4">Back to Dashboard</a>
      </p>
    </body>
    </html>
    """)
