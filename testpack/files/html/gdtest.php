<?php
$test = gd_info();

if (strpos($test, 'GD Version') !== false) {
    echo 'Success';
} else {
    echo 'Failure';
}
?>