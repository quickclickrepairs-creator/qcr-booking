from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/admin")
async def admin():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="en" class="dark">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Quick Click Repairs - Admin</title>
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      <style>
        :root {
          --bg: #1e1e1e;
          --sidebar-bg: #2a2a2a;
          --header-bg: #000;
          --text: #e0e0e0;
          --accent: #00C4B4;
          --card-bg: #2a2a2a;
          --border: #444;
        }
        body {
          margin: 0;
          font-family: 'Segoe UI', Arial, sans-serif;
          background: var(--bg);
          color: var(--text);
        }
        header {
          background: var(--header-bg);
          padding: 12px 24px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          box-shadow: 0 2px 10px rgba(0,0,0,0.6);
          position: sticky;
          top: 0;
          z-index: 1000;
        }
        .logo { font-size: 24px; font-weight: bold; color: var(--accent); }
        .search { background: #333; border: none; border-radius: 20px; padding: 8px 16px; color: white; width: 300px; }
        .user { display: flex; align-items: center; gap: 12px; }
        .user img { width: 36px; height: 36px; border-radius: 50%; }
        .bell { font-size: 20px; cursor: pointer; position: relative; }
        .bell .badge { position: absolute; top: -8px; right: -8px; background: red; color: white; border-radius: 50%; padding: 2px 6px; font-size: 12px; }
        .container { display: flex; min-height: calc(100vh - 60px); }
        nav {
          width: 220px;
          background: var(--sidebar-bg);
          padding: 20px 0;
          border-right: 1px solid var(--border);
        }
        nav a {
          display: block;
          padding: 12px 24px;
          color: #aaa;
          text-decoration: none;
          font-size: 15px;
        }
        nav a:hover { background: var(--accent); color: white; }
        .main-content {
          flex: 1;
          padding: 30px;
        }
        .welcome { font-size: 32px; margin-bottom: 30px; }
        .get-started {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
          gap: 20px;
          margin-bottom: 40px;
        }
        .card {
          background: var(--card-bg);
          padding: 24px;
          border-radius: 12px;
          box-shadow: 0 4px 12px rgba(0,0,0,0.4);
          text-align: center;
        }
        .card h3 { color: var(--accent); margin-bottom: 12px; }
        .btn {
          background: var(--accent);
          color: white;
          padding: 16px;
          border-radius: 8px;
          text-decoration: none;
          font-weight: bold;
          display: block;
          margin-top: 12px;
        }
        .btn:hover { background: #00a89a; }
        .reminders {
          background: var(--card-bg);
          padding: 20px;
          border-radius: 12px;
          margin-bottom: 40px;
        }
        .reminders h3 { color: var(--accent); }
        table {
          width: 100%;
          border-collapse: collapse;
          margin-top: 16px;
        }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid var(--border); }
        th { background: var(--accent); color: black; }
        .charts {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
          gap: 30px;
        }
        .chart-card {
          background: var(--card-bg);
          padding: 20px;
          border-radius: 12px;
        }
      </style>
    </head>
    <body>
      <header>
        <div class="logo">Quick Click Repairs</div>
        <input type="text" class="search" placeholder="Search all the things...">
        <div class="user">
          <span>Alan ▼</span>
          <div class="bell">🔔 <span class="badge">0</span></div>
          <img src="https://i.imgur.com/placeholder-user.jpg" alt="Alan">
        </div>
      </header>

      <div class="container">
        <nav>
          <a href="#">Dashboard</a>
          <a href="#">Organizations</a>
          <a href="#">Invoices</a>
          <a href="#">Customer Purchases</a>
          <a href="#">Refurbs</a>
          <a href="#">Tickets</a>
          <a href="#">Parts</a>
          <a href="#">Inventory</a>
          <a href="#">Purchase Orders</a>
          <a href="#">POS</a>
          <a href="#">Reports</a>
          <a href="#">Admin</a>
          <a href="#">Help</a>
        </nav>

        <div class="main-content">
          <h1 class="welcome">Welcome!</h1>

          <div class="get-started">
            <div class="card">
              <h3>Get Started</h3>
              <a href="/new-customer" class="btn">+ New Customer</a>
              <a href="/new-ticket" class="btn">+ New Ticket</a>
              <a href="/new-checkin" class="btn">+ New Check In</a>
              <a href="/new-invoice" class="btn">+ New Invoice</a>
              <a href="/new-estimate" class="btn">+ New Estimate</a>
            </div>

            <div class="reminders">
              <h3>REMINDERS</h3>
              <table>
                <tr><th>MESSAGE</th><th>TIME</th><th>TECH</th><th>CUSTOMER</th></tr>
                <tr><td>No reminders yet</td><td>-</td><td>-</td><td>-</td></tr>
              </table>
              <button style="margin-top:16px;padding:10px 20px;background:var(--accent);color:black;border:none;border-radius:6px;cursor:pointer">View All</button>
            </div>
          </div>

          <div class="charts">
            <div class="chart-card">
              <h3>Ticket Count per Day (Month to Date)</h3>
              <canvas id="ticketDayChart"></canvas>
            </div>
            <div class="chart-card">
              <h3>Payments by Hour of Day</h3>
              <canvas id="paymentsHourChart"></canvas>
            </div>
          </div>
        </div>
      </div>

      <script>
        // Ticket Count per Day - Bar Chart
        const ctxDay = document.getElementById('ticketDayChart').getContext('2d');
        new Chart(ctxDay, {
          type: 'bar',
          data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
              label: 'Tickets',
              data: [12, 19, 3, 5, 2, 3, 7],
              backgroundColor: '#00C4B4',
              borderColor: '#00a89a',
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: { beginAtZero: true }
            }
          }
        });

        // Payments by Hour - Bar Chart
        const ctxHour = document.getElementById('paymentsHourChart').getContext('2d');
        new Chart(ctxHour, {
          type: 'bar',
          data: {
            labels: ['8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm'],
            datasets: [{
              label: 'Payments',
              data: [2, 5, 8, 12, 15, 10, 8, 6, 4, 2],
              backgroundColor: '#00C4B4',
              borderColor: '#00a89a',
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: { beginAtZero: true }
            }
          }
        });
      </script>
    </body>
    </html>
    """)
