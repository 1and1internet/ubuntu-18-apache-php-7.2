<?php

/*
 * PHP SQLite check.
 */

//Open the database mydb
$db = new SQLite3('mydb');

//drop the table if already exists
$db->exec('DROP TABLE IF EXISTS fhtesting');

//Create a basic table
$db->exec('CREATE TABLE fhtesting (col1 varchar(255))');

//insert rows
$db->exec('INSERT INTO fhtesting (col1) VALUES ("1")');

//Query to ensure insert worked.
$check = $db->exec('SELECT col1 FROM fhtesting');
if ($check)
{
    echo "Success";
} else {
    echo "Failure";
}
?>
