<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Add Driver</title>
  <link rel="stylesheet" href="home.css">
</head>
<body>
  <header>
    <a href="home.html" class="home-button">Home</a>
    <h1>Add Driver</h1>
  </header>

  <main>
    <section id="add-driver">
      <h2>Add a Driver</h2>
      <form id="add-driver" action="" method="post">
        <label for="driverID">Driver ID:</label>
        <input type="text" id="driverID" name="driverID" required>

        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>

        <label for="age">Age:</label>
        <input type="text" id="age" name="age" required>

        <input type="submit" name="stage" value="Add Driver">
        <div class="error" id="passError"></div>
      </form>
    </section>
  </main>

  <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['stage']))
    {
      $driverID = escapeshellarg($_POST['driverID']);
      $name     = escapeshellarg($_POST['name']);
      $age      = (int) $_POST['age'];

      echo exec("python3 project.py add_driver "
      . "$driverID $name $age");
    }
  ?>

  <footer>
  </footer>
</body>
</html>
