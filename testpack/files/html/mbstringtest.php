<?php

   $settings = mb_get_info();

if(!empty($settings))
{
   echo ("Success");
} else {
   echo ("Failure");
}

?>
