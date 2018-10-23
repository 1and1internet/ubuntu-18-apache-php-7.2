<?php
$ver = phpversion();
if ( preg_match("/^7\.2\..*$/", $ver))
{
  echo "Success";
} else {
  echo "Failure";
}

?>
