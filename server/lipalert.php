<?php
$logsfile = "/full/path/to/ipalertlogs.txt";
$potatochips = $_POST["lip"];
echo $potatochips;
exec("nohup pushbullet $potatochips 'GOT IP' > /dev/null 2>&1 &");
$fancytstamp = date("[d/m/Y-H:i:s]");
$f = fopen($logsfile, "a");
fwrite($f, "\n" . $fancytstamp . "\n Got ip: " . $potatochips);
fclose($f);
?>

