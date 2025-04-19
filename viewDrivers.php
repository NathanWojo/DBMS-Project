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
    <section id="view-drivers">
      <h2>Enter Axle Count</h2>
      <form id="view-drivers" action="" method="post">
        <label for="axles">Axles (2 or 3):</label>
        <input type="number" id="axles" name="axles" min="2" max="3" required>

        <input type="submit" name="stage" value="View Drivers">
        <div class="error" id="driverError"></div>
      </form>
    </section>

    <?php
      if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['stage'])) {
        $axles = (int) $_POST['axles'];
        if ($axles === 2 || $axles === 3) {
          exec("python3 project.py view_drivers $axles", $lines, $status);

          if ($status !== 0) {
            echo "<p class='error'>Error running Python: exit code $status</p>";
          } else {
            echo "<pre>";
            echo htmlspecialchars(implode("\n", $lines));
            echo "</pre>";
          }
        } else {
          echo "<p class='error'>Invalid input. Please enter 2 or 3.</p>";
        }
      }
    ?>
  </main>

  <footer></footer>
</body>
</html>