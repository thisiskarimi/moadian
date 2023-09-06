<?php
    $hex = $argv[1];
    $iv = $argv[2];
    $key = hex2bin($hex);
    $iv = hex2bin($iv);
    $source = $argv[3];
    $sourceLength = strlen($source);
    $keyLength = strlen($key);
    $result = '';
    for ($i = 0;$i < $sourceLength;$i++)
    {
        $result .= $source[$i] ^ $key[$i % $keyLength];
    }
    $tag = '';
    $cipherText = openssl_encrypt($result, "aes-256-gcm", $key, OPENSSL_RAW_DATA, $iv, $tag, "", 16);
    $result = base64_encode($cipherText . $tag);
    echo $result;
    exit(0);
