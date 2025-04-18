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
