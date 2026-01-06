@app.get("/new-ticket")
async def new_ticket(request: Request):
    return HTMLResponse("""
    <div style="max-width:800px;margin:auto;background:#2a2a2a;padding:40px;border-radius:15px;color:#e0e0e0">
      <h1 style="text-align:center;color:#00C4B4;margin-bottom:30px">+ New Ticket</h1>
      <form action="/create-ticket" method="post">
        <h2 style="color:#00C4B4">Customer</h2>
        <input name="customer_name" placeholder="Full Name" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="customer_email" type="email" placeholder="Email" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="customer_phone" placeholder="Phone Number" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>

        <h2 style="color:#00C4B4">Device</h2>
        <input name="device_type" placeholder="Type (Laptop/Phone/etc)" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="brand" placeholder="Brand" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="model" placeholder="Model" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white" required>
        <input name="serial" placeholder="Serial/IMEI" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <input name="password" placeholder="Password/PIN" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">

        <h2 style="color:#00C4B4">Faults (check all that apply)</h2>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px">
          <label><input type="checkbox" name="faults" value="No Power"> No Power</label>
          <label><input type="checkbox" name="faults" value="Won't Charge"> Won't Charge</label>
          <label><input type="checkbox" name="faults" value="Cracked Screen"> Cracked Screen</label>
          <label><input type="checkbox" name="faults" value="Liquid Damage"> Liquid Damage</label>
          <label><input type="checkbox" name="faults" value="Slow Performance"> Slow Performance</label>
          <label><input type="checkbox" name="faults" value="Virus/Malware"> Virus/Malware</label>
          <label><input type="checkbox" name="faults" value="No WiFi"> No WiFi</label>
          <label><input type="checkbox" name="faults" value="Other"> Other</label>
        </div>
        <input name="other_fault" placeholder="Describe 'Other' fault" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">

        <h2 style="color:#00C4B4">Pricing</h2>
        <input name="labour_price" type="number" step="0.01" placeholder="Labour £" value="45.00" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">
        <input name="parts_price" type="number" step="0.01" placeholder="Parts £" value="0.00" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white">

        <h2 style="color:#00C4B4">Notes</h2>
        <textarea name="notes" rows="4" placeholder="Additional notes" style="width:100%;padding:14px;margin:10px 0;border-radius:8px;background:#333;color:white"></textarea>

        <button type="submit" style="background:#00C4B4;color:white;padding:18px;font-size:22px;border:none;border-radius:10px;width:100%;margin-top:20px;cursor:pointer">CREATE TICKET</button>
      </form>
      <p style="text-align:center;margin-top:30px"><a href="/admin" style="color:#00C4B4">← Back to Dashboard</a></p>
    </div>
    """)

@app.post("/create-ticket")
async def create_ticket(
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    customer_phone: str = Form(...),
    device_type: str = Form(...),
    brand: str = Form(...),
    model: str = Form(...),
    serial: str = Form(""),
    password: str = Form(""),
    faults: list[str] = Form([]),
    other_fault: str = Form(""),
    labour_price: float = Form(45.0),
    parts_price: float = Form(0.0),
    notes: str = Form("")
):
    total = labour_price + parts_price
    all_faults = ", ".join(faults)
    if other_fault:
        all_faults += f", {other_fault}"
    return HTMLResponse(f"""
    <div style="max-width:800px;margin:auto;background:#2a2a2a;padding:40px;border-radius:15px;color:#e0e0e0">
      <h1 style="color:green;text-align:center">TICKET CREATED!</h1>
      <h2 style="text-align:center">Customer: {customer_name}</h2>
      <p style="text-align:center;font-size:24px">
        Device: {brand} {model} ({device_type})<br>
        Serial: {serial}<br>
        Faults: {all_faults or 'None specified'}<br>
        Labour: £{labour_price:.2f}<br>
        Parts: £{parts_price:.2f}<br>
        <strong>Total: £{total:.2f}</strong>
      </p>
      <p style="text-align:center;margin-top:50px">
        <a href="/admin" style="color:#00C4B4">← Back to Dashboard</a>
      </p>
    </div>
    """)
