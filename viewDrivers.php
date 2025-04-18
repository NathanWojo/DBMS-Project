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
    <a href="home.html" class="home-button">
        <svg width="20px" height="20px" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M1 6V15H6V11C6 9.89543 6.89543 9 8 9C9.10457 9 10 9.89543 10 11V15H15V6L8 0L1 6Z" fill="#FFFFFF"/>
        </svg>
    </a>
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
