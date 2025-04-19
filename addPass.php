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
    <a href="home.html" class="home-button">
        <svg width="20px" height="20px" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M1 6V15H6V11C6 9.89543 6.89543 9 8 9C9.10457 9 10 9.89543 10 11V15H15V6L8 0L1 6Z" fill="#FFFFFF"/>
        </svg>
    </a>
    <h1>Add Driver</h1>
  </header>

  <main>
    <section id="add-driver">
      <h2>Add a Driver</h2>
      <form id="add-driver" action="" method="post">
        <!-- Driver info -->
        <label for="driverID">Driver ID:</label>
        <input type="text" id="driverID" name="driverID" required>

        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>

        <label for="age">Age:</label>
        <input type="number" id="age" name="age" required>

        <!-- Vehicle info -->
        <label for="licensePlate">License Plate:</label>
        <input type="text" id="licensePlate" name="licensePlate" required>

        <label for="make">Make:</label>
        <input type="text" id="make" name="make" required>

        <label for="model">Model:</label>
        <input type="text" id="model" name="model" required>

        <label for="axles">Axles (2 or 3):</label>
        <input type="number" id="axles" name="axles" min="2" max="3" required>

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

      $licensePlate = escapeshellarg($_POST['licensePlate']);
      $make         = escapeshellarg($_POST['make']);
      $model        = escapeshellarg($_POST['model']);
      $axles        = (int) $_POST['axles'];

      echo exec("python3 project.py add_driver "
        . "$driverID $name $age $licensePlate $make $model $axles");
    }
  ?>

  <footer>
  </footer>
</body>
</html>