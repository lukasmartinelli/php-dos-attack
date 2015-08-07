#!/usr/bin/php
<?php
    $filename = $argv[1];
    $file = file_get_contents($filename);
    $hashes = explode("\n", $file);
    $size = count($hashes);

    $array = array();
    for($key = 0; $key < $size; $key++) {
        $array[strval($key)] = 0;
    }
    $serialized = serialize($array);

    $startTime = microtime(true);
    $array = unserialize($serialized);
    $endTime = microtime(true);

    echo 'Unserializing ', $size, ' good elements took ', $endTime - $startTime, ' seconds', "\n";

    $array = array();
    foreach($hashes as $key) {
        $array[$key] = 0;
    }
    $serialized = serialize($array);
    $startTime = microtime(true);
    $array = unserialize($serialized);
    $endTime = microtime(true);

    echo 'Unserializing ', $size, ' evil elements took ', $endTime - $startTime, ' seconds', "\n";
?>
