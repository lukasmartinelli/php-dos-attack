<?php
    header('Content-Type: application/json');

    $body = file_get_contents('php://input');
    $params = json_decode($body);
    $response = array('name' => $params->{'name'}, 'email' => $params->{'email'});
    echo json_encode($response);
?>
