Simulate Hash Collision Attack on a PHP Server
==============================================

[Vagrant](https://www.vagrantup.com/downloads) is used to automatically create
a PHP webserver VM.
Vagrant will keep the `server` folder in sync with `/var/www/html` for easy testing.
You also need [Ansible](http://docs.ansible.com/intro_installation.html) to provision the server.

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
Install the requirements:

```
pip install -r requirements.txt
```

The `attack.py` script will make parallel requests (amount can be specified with --count`)
to a URL endpoint. It reads collisions from given text file and tries to do a
Hash collision Attack with them. You can set the attack type to either use form fields
or a json map.

Make one request to the webserver in the VM.

```
python attack.py http://localhost:8080/index.php hashes.txt
```

Make a normal request to compare with the collision attack.

```
python attack.py http://localhost:8080/index.php hashes.txt --no-collide
```

Make 100 requests to a fake JSON api.

```
python attack.py http://localhost:8080/index.php hashes.txt --count=100 --type=json
```

Test PHP vulnerabilities to Collision Attacks
---------------------------------------------

In the directory `test` there are PHP scripts that demonstrate vulnerabilities of
functions that use the PHP map.

Run a script with `hashes.txt`:

```
php array.php hashes.txt
```
