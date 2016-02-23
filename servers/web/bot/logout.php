<?php
session_start();
$_SESSION = array();
header("Location: login.php");
?>