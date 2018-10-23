<?php

$xml = new SimpleXMLElement('<?xml version="1.0" encoding="utf-8"?><mydoc></mydoc>');

$xml->addAttribute('version', '1.0');
$xml->addChild('datetime', date('Y-m-d H:i:s'));

$person = $xml->addChild('person');
$person->addChild('firstname', 'John');
$person->addChild('secondname', 'Doe');
$person->addChild('telephone', '0123456789');
$person->addChild('email', 'me@something.com');

$address = $person->addchild('address');
$address->addchild('homeaddress', '12 Suburbia Close, Townville');
$address->addChild('workaddress', '1000 Main Street, Cityville');

$dom_sxe = dom_import_simplexml($xml);
if (!$dom_sxe) {
    echo 'Error while converting XML';
    exit;
}

$dom = new DOMDocument('1.0');
$dom_sxe = $dom->importNode($dom_sxe, true);
$dom_sxe = $dom->appendChild($dom_sxe);

$filename = './test.xml';

$dom->save($filename);

if (file_exists($filename)) {
    echo "Success";
} else {
    echo "Failure";
}

?>
