Simulate Hash Collision Attack on a PHP Server
==============================================

[Vagrant](https://www.vagrantup.com/downloads) is used to automatically create
a PHP webserver VM.
Vagrant will keep the `server` folder in sync with `/var/www/html` for easy testing.

Start server
------------

Download and start the VM:
```
vagrant up
```

Vagrant will map the port `80` of the webserver to `8080`.
Therefore you can visit your site at `localhost:8080`.

Run a Hash Collision Attack
---------------------------

The `attack.py` script will make POST requests with all the collision in `hashes.txt`.

Instruct the attack.py to make 100 requests to `http://localhost:8080` with the
collision values in `hashes.txt` and using `form` fields:
```
python attack.py http://localhost:8080 hashes.txt 100 form
```

Test PHP vulnerabilities to Collision Attacks
---------------------------------------------

In the directory `test` there are PHP scripts that demonstrate vulnerabilities of
functions that use the PHP map.

Run a script with `hashes.txt`:
```
php array.php hashes.txt
```
