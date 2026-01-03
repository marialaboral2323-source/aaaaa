<?php
$data = '';
if ($_SERVER['REQUEST_METHOD'] === 'GET'){
    $data = $_GET['text'] ?? "Error: 'text' variable not found in GET body.";
}
echo $data;
?>
