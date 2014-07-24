<?php
    header('Content-Type: application/json');
    $body = http_get_request_body()
    $params = json_decode($body)

    $response = array('name' => $params['name'], 'email' => $params['email'])
    echo json_encode($response)
?>
