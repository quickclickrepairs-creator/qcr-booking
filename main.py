<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Quick Click Repairs – Dashboard</title>
  <style>
    * {margin:0;padding:0;box-sizing:border-box}
    body {font-family: 'Segoe UI', Arial, sans-serif; background:#1e1e1e; color:#e0e0e0; margin:0}
    header {background:#000; padding:15px 30px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 4px 10px rgba(0,0,0,0.5)}
    header h1 {color:#fff; font-size:24px}
    .search {background:#333; border-radius:20px; padding:8px 15px; color:white; border:none; width:300px}
    .user {display:flex; align-items:center; gap:10px}
    .user img {width:40px; height:40px; border-radius:50%}
    nav {background:#2a2a2a; padding:20px; min-width:200px}
    nav ul {list-style:none}
    nav li {margin:10px 0}
    nav a {color:#aaa; text-decoration:none; font-size:16px; display:block; padding:10px; border-radius:8px}
    nav a:hover {background:#00C4B4; color:white}
    .main {display:flex}
    .content {flex:1; padding:30px}
    .welcome {font-size:36px; margin-bottom:40px}
    .get-started {display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:20px; margin-bottom:40px}
    .btn {background:#00C4B4; color:white; padding:30px; border-radius:12px; text-decoration:none; font-size:20px; font-weight:bold; text-align:center; display:flex; align-items:center; justify-content:center; gap:15px}
    .btn:hover {background:#00a89a}
    .icon {font-size:32px}
    .reminders {background:#2a2a2a; padding:25px; border-radius:12px}
    .reminders h2 {margin-bottom:20px}
    table {width:100%; border-collapse:collapse}
    th {background:#00C4B4; color:white; padding:12px; text-align:left}
    td {padding:12px; border-bottom:1px solid #444}
  </style>
</head>
<body>
  <header>
    <h1>Quick Click Repairs</h1>
    <input type="text" placeholder="Search all the things" class="search">
    <div class="user">
      <span>Alan ▼</span>
      <img src="https://i.imgur.com/placeholder-user.jpg" alt="User">
    </div>
  </header>
  <div class="main">
    <nav>
      <ul>
        <li><a href="#">Organizations</a></li>
        <li><a href="#">Invoices</a></li>
        <li>
