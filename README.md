# Simulate Hash Collision Attack on a PHP Server

[Vagrant](https://www.vagrantup.com/downloads) is used to automatically create
a PHP webserver VM.
Vagrant will keep the `server` folder in sync with `/var/www/html` for easy testing.
You also need [Ansible](http://docs.ansible.com/intro_installation.html) to provision the server.

## Start server


Download and start the VM:

```
vagrant up
```

Vagrant will map the port `80` of the webserver to `8080`.
Therefore you can visit your site at `localhost:8080`.

## Run a Hash Collision Attack

Install the requirements:

```
pip install -r requirements.txt
```

The `attack.py` script will make parallel requests (amount can be specified with `--count`)
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
python attack.py http://localhost:8080/api.php hashes.txt --count=100 --type=json
```

## Test PHP vulnerabilities to Collision Attacks

In the directory `test` there are PHP scripts that demonstrate vulnerabilities of
functions that use the PHP map.

### Create smaller test set

The file `collision_keys` contains precomputed colliding keys. To create
a smaller set of keys for easy testing you can create a new file:

```
head -n 10000 collision_keys.txt > collision_keys_small.txt
```

### Insert into Array

Run tests for inserting colliding keys into array:

```
php test/array.php collision_keys.txt
```

Results:

```
Inserting 65537 evil elements took 37.624982833862 seconds
Inserting 65537 good elements took 0.02390193939209 seconds
```

### Reading JSON

Run tests for calling `json_decode` for JSON key-value pairs with colliding keys:

```
php test/json_decode.php collision_keys.txt
```

Results:

```
Decoding 65537 evil elements took 36.51837182045 seconds
Decoding 65537 good elements took 0.012500047683716 seconds
```

### Unserializing PHP Objects

Run tests when `unserializing` an array with colliding keys:

```
php test/unserialize.php collision_keys.txt
```

Results:

```
Unserializing 65537 evil elements took 30.025561094284 seconds
Unserializing 65537 good elements took 0.0123610496521 seconds
```

### XML Parsing

Run tests when parsing XML with elements name that should collide with each other
into a class with `xml_parse_into_struct`:

```
php test/xml_parse_into_struct.php collision_keys.txt
```

Results:

```
Parsing 65537 evil elements took 0.00072693824768066 seconds
Parsing 65537 good elements took 0.00044703483581543 seconds
```

## Plot time difference

You can generate the plot data used for the diagrams by yourself:

```
php plot/array.php collision_keys.txt
```

Sample Results:

```
elements,evilTime,goodTime
0,4.0531158447266E-6,1.9073486328125E-6
500,0.00217604637146,0.00029802322387695
1000,0.0081908702850342,0.00053691864013672
1500,0.015079021453857,0.0008399486541748
2000,0.019697189331055,0.00064301490783691
2500,0.033805131912231,0.00084710121154785
3000,0.04535698890686,0.00096511840820312
3500,0.058545112609863,0.0010898113250732
4000,0.077980995178223,0.0012860298156738
4500,0.099925994873047,0.0014569759368896
```

