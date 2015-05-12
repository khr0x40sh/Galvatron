<?php
$dir="default";
echo get_current_user();
#echo $_GET["idu"]."\nP:".$_POST["idu"];
if($_GET["idu"] !="")
{
	$dir=$_GET["idu"];
	$create= "/var/www/upload/".$dir;
	#exec("mkdir -m 0777 ".$create);
	if (!mkdir($create, 0777, true)) {
    		die('Failed to create folders...');
	}
}

if ($_FILES["file"]["error"] > 0)
{
echo "Error: " . $_FILES["file"]["error"]."<br/>";
}
else
{
echo "Upload: ".$_FILES["file"]["name"]."<br/>";
echo "Type: ".$_FILES["file"]["type"]."<br/>";
echo "Size: ". ($_FILES["file"]["size"]/1024)." Kb<br/>";
echo "Temp: ". $_FILES["file"]["tmp_name"]."<br/>";

move_uploaded_file($_FILES["file"]["tmp_name"], "upload/".$dir."/".$_FILES["file"]["name"]);
echo "Stored in:  upload/".$dir."/".$_FILES["file"]["name"]."<br/>";
}
?>
