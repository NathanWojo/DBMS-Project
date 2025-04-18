<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Add Pass</title>
  <link rel="stylesheet" href="home.css">
</head>
<body>
  <header>
    <a href="home.html" class="home-button">Home</a>
    <h1>Add Pass</h1>
  </header>

  <main>
    <section id="add-driver">
      <h2>1) Add a Pass</h2>
      <form id="add-driver" action="" method="post">
        <label for="passID">Pass ID:</label>
        <input type="text" id="passID" name="passID" required>

        <label for="LicensePlate">License Plate:</label>
        <input type="text" id="LicensePlate" name="LicensePlate" required>

        <label for="driverID">Driver ID:</label>
        <input type="text" id="driverID" name="driverID" required>

        <label for="plazaNumber">Plaza Number:</label>
        <input type="text" id="plazaNumber" name="plazaNumber" required>

        <label for="passDate">Pass Date(FIX LATER):</label>
        <input type="text" id="passDate" name="passDate" required>

        <label for="passTime">Pass Time(FIX LATER):</label>
        <input type="text" id="passTime" name="passTime" required>

        <label for="cost">Cost(FIX LATER):</label>
        <input type="text" id="cost" name="cost" required>

        <input type="submit" name="stage" value="Add Pass">
        <div class="error" id="passError"></div>
      </form>
    </section>
  </main>

  <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['stage']))
    {
      $passID = escapeshellarg($_POST['passID']);
      $LicensePlate     = escapeshellarg($_POST['LicensePlate']);
      $driverID     = escapeshellarg($_POST['driverID']);
      $plazaNumber     = escapeshellarg($_POST['plazaNumber']);
      $passDate     = escapeshellarg($_POST['passDate']);
      $passTime     = escapeshellarg($_POST['passTime']);
      $cost      = (float) $_POST['cost'];

      echo exec("python3 project.py add_pass "
      . "$passID $LicensePlate $driverID $plazaNumber $passDate $passTime $cost");
    }
  ?>

  <footer>
  </footer>
</body>
</html>
