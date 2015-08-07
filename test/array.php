#!/usr/bin/php
<?php
    # Source: http://nikic.github.io/2011/12/28/Supercolliding-a-PHP-array.html
    # Hash Algorithm: http://www.phpinternalsbook.com/hashtables/hash_algorithm.html
    # Chaos Pres: http://events.ccc.de/congress/2011/Fahrplan/attachments/2007_28C3_Effective_DoS_on_web_application_platforms.pdf
    $filename = $argv[1];
    $file = file_get_contents($filename);
    $hashes = explode("\n", $file);
    $size = count($hashes);

    $startTime = microtime(true);
    $array = array();
    for($key = 0; $key < $size; $key++) {
        $array[strval($key)] = 0;
    }
    $endTime = microtime(true);

    echo 'Inserting ', $size, ' good elements took ', $endTime - $startTime, ' seconds', "\n";

    $startTime = microtime(true);
    $array = array();
    foreach($hashes as $key) {
        $array[$key] = 0;
    }
    $endTime = microtime(true);

    echo 'Inserting ', $size, ' evil elements took ', $endTime - $startTime, ' seconds', "\n";
?>
