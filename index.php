<html>
    <body>
        <?php if ($_SERVER['REQUEST_METHOD'] === 'GET') { ?>
            <form action="index.php" method="post">
                Name: <input type="text" name="name"><br>
                E-mail: <input type="text" name="email"><br>
                <input type="submit">
            </form>
        <?php } else if ($_SERVER['REQUEST_METHOD'] === 'POST') { ?>
            Welcome <?php echo $_POST["name"]; ?><br>
            Your email address is: <?php echo $_POST["email"]; ?>
        <?php } ?>
    </body>
</html>
