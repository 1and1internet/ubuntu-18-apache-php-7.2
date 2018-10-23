<?php
$test = gd_info();

foreach ($test as $key => $value) {
  if ($key == 'GD Version') {
    echo "Success";
    exit;
  }
}

echo 'Failure';
?>
