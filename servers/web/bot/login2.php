<?php
 /******************************************************************************************
           ____    ____                        ____  ____                       __  
          |_   \  /   _|                      |_   ||   _|                     |  ] 
            |   \/   |   .--.   _ .--.   .--.   | |__| |   ,--.   _ .--.   .--.| |  
            | |\  /| | / .'`\ \[ `.-. |/ .'`\ \ |  __  |  `'_\ : [ `/'`\]/ /'`\' |  
           _| |_\/_| |_| \__. | | | | || \__. |_| |  | |_ // | |, | |    | \__/  |  
          |_____||_____|'.__.' [___||__]'.__.'|____||____|\'-;__/[___]    '.__.;__] . .   .-.    . 
                                                                                    | |   |\|   '| 
                 By Carlos Ganoza || www.todoporelvicio.com                         `.'   `-' .  '
 ******************************************************************************************/
session_start();
// Configura los datos de tu cuenta
require ("conexion.php");
if ($_POST['user']) {
//Comprobacion del envio del nombre de usuario y password
$user=$_POST['user'];
$pass=$_POST['password'];
$password= md5 ($pass); 
if ($password==NULL) {
header('Location: login.php?error=2');
}else{
$query = mysql_query("SELECT user,password FROM admin WHERE user = '$user'") or die(mysql_error());
$data = mysql_fetch_array($query);
if($data['password'] != $password) {

header('Location: login.php?error=1');
}else{
$query = mysql_query("SELECT user,password FROM admin WHERE user = '$user'") or die(mysql_error());
$row = mysql_fetch_array($query);
$_SESSION["sesion"] = $row['user'];

//echo "<p>";
//echo "<p>";
//echo "<p>";
header('Location: cpanel.php');

}
}
}
?>
