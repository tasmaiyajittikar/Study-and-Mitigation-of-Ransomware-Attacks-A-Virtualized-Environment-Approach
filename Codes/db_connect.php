<?php
$servername = "localhost";
$username = "phpmyadmin";
$password = "solo";  // or your MySQL password
$dbname = "ransomware_db";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>