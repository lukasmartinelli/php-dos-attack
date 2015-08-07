#!/usr/bin/php
<?php
    $filename = $argv[1];
    $file = file_get_contents($filename);
    $hashes = explode("\n", $file);
    $size = count($hashes);

    $xml = "<array>";
    foreach($hashes as $key) {
        if($key != "") {
            $xml .= "<" . $key . ">0</" . $key . ">";
        }
    }

    $xml .= "</array>";
    $p = xml_parser_create();
    $startTime = microtime(true);
    xml_parse_into_struct($p, $xml, $vals, $index);
    xml_parser_free($p);
    $endTime = microtime(true);

    echo 'Parsing ', $size, ' good elements took ', $endTime - $startTime, ' seconds', "\n";

    $xml = "<array>";
    foreach($hashes as $key) {
        if($key != "") {
            $xml .= "<" . $key . ">0</" . $key . ">";
        }
    }
    $xml .= "</array>";

    $p = xml_parser_create();
    $startTime = microtime(true);
    xml_parse_into_struct($p, $xml, $vals, $index);
    xml_parser_free($p);
    $endTime = microtime(true);

    echo 'Parsing ', $size, ' evil elements took ', $endTime - $startTime, ' seconds', "\n";
?>
