<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>View Plazas</title>
  <link rel="stylesheet" href="home.css">
</head>
<body>
  <header>
    <a href="home.html" class="home-button">Home</a>
    <h1>View Plazas</h1>
  </header>

  <main>
    <section id="view-plazas">
      <h2>View Plazas</h2>
      <form id="view-plaza" action="" method="post">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>

        <input type="submit" name="stage" value="View Plazas">
        <div class="error" id="passError"></div>
      </form>
    </section>
  </main>

  <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['stage']))
    {
      $name     = escapeshellarg($_POST['name']);

      exec("python3 project.py view_plazas " . "$name", $lines, $status);
      
      if ($status !== 0) {
        echo "<p class='error'>Error running Python: exit code $status</p>";
      } else {
        echo "<pre>";
        echo htmlspecialchars(implode("\n", $lines));
        echo "</pre>";
      }
    }
  ?>

  <footer>
  </footer>
</body>
</html>
