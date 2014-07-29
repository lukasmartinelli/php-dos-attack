#!/usr/bin/php
<?php
    $filename = $argv[1];
    $file = file_get_contents($filename);
    $lines = explode("\n", $file);

    function measureEvilElements($elements) {
        $startTime = microtime(true);
        $array = array();
        foreach($elements as $key) {
            $array[$key] = 0;
        }
        $endTime = microtime(true);
        return $endTime - $startTime;
    }

    function measureGoodElements($elements) {
        $startTime = microtime(true);
        $array = array();
        for($key = 0; $key < count($elements); $key++) {
            $array[strval($key)] = 0;
        }
        $endTime = microtime(true);
        return $endTime - $startTime;
    }

    echo 'elements', 'evilTime', 'goodTime', "\r\n";
    for($i = 0; $i < count($lines); $i+=50) {
        $keys = array_slice($lines, 0, $i);
        $evilTime = measureEvilElements($keys);
        $goodTime = measureGoodElements($keys);
        echo $i, ',', $evilTime, ',', $goodTime, "\r\n";
    }
?>
