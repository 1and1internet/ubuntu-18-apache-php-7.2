<?php

//create curl session
$ch = curl_init();

// set the url to fetch 
curl_setopt($ch, CURLOPT_URL, "https://www.google.co.uk");

//return the HTTP Response header
curl_setopt($ch, CURLOPT_HEADER, true);

//don't return the body
curl_setopt($ch, CURLOPT_NOBODY, true);

//return the transfer (the result of curl_exec()) as a string instead of outputing directly
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

//set timeout for request.
curl_setopt($ch, CURLOPT_TIMEOUT,10);

// execute the curl session
curl_exec($ch);

//get the http code.
$httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

// close curl resource to free up system resources 
curl_close($ch);

//check we get a code
if ($httpcode)
{       
    echo "Success";
} else { 
    echo "Failure";
}
?>