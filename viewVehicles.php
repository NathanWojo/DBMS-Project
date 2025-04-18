<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>View Vehicles</title>
  <link rel="stylesheet" href="home.css">
</head>
<body>
  <header>
    <a href="home.html" class="home-button">Home</a>
    <h1>View Vehicles</h1>
  </header>

  <main>
    <section id="view-vehicles">
      <h2>View Vehicles</h2>
    </section>
  </main>

  <?php
    echo exec("python3 project.py view_vehicles");
  ?>

  <footer>
  </footer>
</body>
</html>
