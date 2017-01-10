<?php
    if (!isset($_POST['user']) || !isset($_POST['pw'])) 
        $logined = 0;
    else if (check_user($_POST['user']) && check_pw($_POST['pw']))
        $logined = 1;
    else
        $logined = 2;
?>
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <title>orangr</title>
    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <script src="js/bootstrap.min.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta charset="utf-8" />
    <link href="https://fonts.googleapis.com/css?family=Inconsolata" rel="stylesheet">
</head>
<body>
    <div class="container-fluid text-center">
        <div class="row" style="padding-top: 50px;">
<?php       if ($logined == 1) { ?>
            <div class="alert alert-dismissible alert-success">
                <button type="button" class="close" data-dismiss="alert">&times;</button>
                <strong>Logined success!</strong> flag: CTF{ORangr_ANDangr_XORangr_NOTangr}
            </div>
<?php       } ?>
<?php       if ($logined == 2) { ?>
            <div class="alert alert-dismissible alert-danger">
                <button type="button" class="close" data-dismiss="alert">&times;</button>
                <strong>Login failed. QQ</strong>
            </div>
<?php       } ?>
            <div class="col-md-offset-4 col-md-4">
                <h3>: ( Hack me : )</h3>
                <a href="http://angr.io/"><img src="http://angr.io/img/angry_face.png"></a>
                <form role="form" method="post" action="index.php">
                    <div class="form-group">
                        <label for="user">Username</label>
                        <input type="text" class="form-control" id="user" name="user">
                    </div>
                    <div class="form-group">
                        <label for="pw">Password</label>
                        <input type="password" class="form-control" id="pw" name="pw">
                    </div>
                    <button type="submit" class="btn btn-default btn-block">Login</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
