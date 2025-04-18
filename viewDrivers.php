<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>View Drivers</title>
  <link rel="stylesheet" href="home.css">
</head>
<body>
  <header>
    <a href="home.html" class="home-button">Home</a>
    <h1>View Drivers</h1>
  </header>

  <main>
    <section id="view-vehicles">
      <h2>View Drivers</h2>
    </section>
  
    <?php
      exec("python3 project.py view_drivers", $lines, $status);
        
      if ($status !== 0) {
        echo "<p class='error'>Error running Python: exit code $status</p>";
      } else {
        echo "<pre>";
        echo htmlspecialchars(implode("\n", $lines));
        echo "</pre>";
      }
    ?>
  </main>

  <footer>
  </footer>
</body>
</html>
