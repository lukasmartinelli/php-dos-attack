#!/bin/sh
wget http://museum.php.net/php5/php-5.3.8.tar.gz
tar zxf php-5.3.8.tar.gz
cd php-5.3.8
./configure --disable-libxml --disable-dom --disable-simplexml --disable-xml --disable-xmlreader --disable-xmlwriter --without-pear
make
sudo make install
