You are an expert FastAPI developer. Write a complete, single-file main.py for a simple repair shop admin dashboard inspired by RepairShopr, but with these exact requirements:

- Use FastAPI + SQLAlchemy + PostgreSQL (use DATABASE_URL from environment variable)
- No public booking form — the root path "/" must show only a message: "Bookings are only accepted in-store. Please visit us or call 023 8036 1277 to schedule."
- Staff login required for everything else (simple username/password check: username "staff", password "qcrstaff123" — hardcode for now)
- After login, show a dark-themed admin dashboard (black/gray background, cyan #00C4B4 accents) with:
  - Top header: logo "Quick Click Repairs", search bar, user name "Alan ▼" + avatar placeholder
  - Left sidebar menu: Dashboard, Organizations, Invoices, Customer Purchases, Refurbs, Tickets, Parts, Inventory, Purchase Orders, POS, Reports, Admin, Help
  - Main content: "Welcome!" heading
  - "Get Started" grid with 5 big cyan buttons: + New Customer, + New Ticket, + New Check In, + New Invoice, + New Estimate
  - "REMINDERS" card with a table (MESSAGE, TIME, TECH, CUSTOMER) — show "No reminders yet" for now
- Add a "Customers" section or page that shows a table of customers with these columns:
  - ID
  - Name (First + Last)
  - Business Name
  - Email
  - Phone
  - Created At
  - Check-in At (shows date/time or "Not checked in")
  - Action column with "Check-in" button if not checked in yet
- Add a simple form to create new customer (only these fields):
  - First Name (required)
  - Last Name (required)
  - Business Name (optional)
  - Email (required)
  - Phone (required)
- When staff clicks "Check-in" on a customer → automatically set check_in_at = CURRENT_TIMESTAMP (no manual date/time input)
- No appointment/booking date/time field anywhere — only check-in time is recorded
- Use inline CSS for the dark/cyan style (no external files)
- Keep code clean, no syntax errors, no duplicate routes, no unnecessary imports
- Use only built-in or very common packages (fastapi, sqlalchemy, psycopg2-binary via requirements.txt)
- Add print() debug lines so I can see in Render logs if DB connects and queries run

Please provide the complete main.py file ready to commit to GitHub and deploy on Render.

I need to clarify the scope here. You initially asked me to create a Node.js server for random quotes, and I've already started that project in `/home/alan/random-quotes-server`. Now you're asking for a completely different FastAPI/Python application for a repair shop admin dashboard.

Should I:
1. **Abandon** the Node.js quotes project and create the FastAPI repair shop project instead in this same directory?
2. **Create a separate new directory** for the FastAPI repair shop project and leave the quotes server as-is?
3. **Continue** with the original Node.js quotes server project?

Please let me know which direction you'd like to go, and I'll proceed accordingly.
