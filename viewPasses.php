<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>View Toll Passes</title>
  <link rel="stylesheet" href="home.css">
</head>
<body>
  <header>
    <a href="home.html" class="home-button">
        <svg width="20px" height="20px" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M1 6V15H6V11C6 9.89543 6.89543 9 8 9C9.10457 9 10 9.89543 10 11V15H15V6L8 0L1 6Z" fill="#FFFFFF"/>
        </svg>
    </a>
    <h1>View Toll Passes</h1>
  </header>

  <main>
    <section id="view-passes">
      <h2>View Passes</h2>
      <form id="view-passes" action="" method="post">
        <label for="plazaNumber">Plaza Number:</label>
        <input type="text" id="plazaNumber" name="plazaNumber" required>

        <input type="submit" name="stage" value="View Passes">
        <div class="error" id="passError"></div>
      </form>
    </section>
    <?php
      if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['stage']))
      {
        $plazaNumber     = escapeshellarg($_POST['plazaNumber']);
        
        exec("python3 project.py view_passes " . "$plazaNumber", $lines, $status);
        
        if ($status !== 0) {
          echo "<p class='error'>Error running Python: exit code $status</p>";
        } else {
          echo "<pre>";
          echo htmlspecialchars(implode("\n", $lines));
          echo "</pre>";
        }
      }
    ?>
  </main>

  <footer>
  </footer>
</body>
</html>
