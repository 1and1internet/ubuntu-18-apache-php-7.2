<?php

$zip = new ZipArchive();
$filename = "./test123.zip";

if ($zip->open($filename, ZipArchive::CREATE)!==TRUE) {
    exit("cannot open <$filename>\n");
}

$zip->addFromString("testfilephp.txt" . time(), "#1 This is a test string added as testfilephp.txt.\n");
$zip->addFromString("testfilephp2.txt" . time(), "#2 This is a test string added as testfilephp2.txt.\n");

if ($zip->status == 0) {
    echo "Success";
} else {
    echo "Failure";
}

$zip->close();
?>
