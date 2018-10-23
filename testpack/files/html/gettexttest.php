<?php

if ((extension_loaded('gettext')) and (function_exists("gettext"))) {
    echo "Success";
} else {
    echo "Failure";
}

?>
