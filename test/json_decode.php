#!/usr/bin/php
<?php
    $filename = $argv[1];
    $file = file_get_contents($filename);
    $hashes = explode("\n", $file);
    $size = count($hashes);

    $array = array();
    foreach($hashes as $key) {
        $array[$key] = 0;
    }
    $json = json_encode($array);
    $startTime = microtime(true);
    $array = json_decode($json);
    $endTime = microtime(true);

    echo 'Decoding ', $size, ' evil elements took ', $endTime - $startTime, ' seconds', "\n";

    $array = array();
    for($key = 0; $key < $size; $key++) {
        $array[strval($key)] = 0;
    }
    $json = json_encode($array);

    $startTime = microtime(true);
    $array = json_decode($json);
    $endTime = microtime(true);

    echo 'Decoding ', $size, ' good elements took ', $endTime - $startTime, ' seconds', "\n";
?>
