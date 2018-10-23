<?php

if ((extension_loaded('mysqli')) and (function_exists("mysqli_connect"))) {
    echo "Success";
} else {
    echo "Failure";
}

?>
