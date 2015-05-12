<?php
$link=mysql_connect("127.0.0.1", "botnet", "1qazXSW@");
if (!$link)
{
	die('Not conn: ' . mysql_error());
}
$db_c = mysql_select_db("bot",$link);
if (!$db_c) {
    die ('Can\'t use foo : ' . mysql_error());
}
?>