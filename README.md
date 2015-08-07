# Simulate Hash Collision Attack on a PHP Server

Checkout the [associated blog post](http://lukasmartinelli.ch/web/2014/11/17/php-dos-attack-revisited.html).

## How it works

Nowadays every web application uses a JSON API, which is still vulnerable to complexity attacks if you use PHP.

![Insert Animation](http://lukasmartinelli.ch/media/hash-collisions.gif)

## Run the server

```
docker run -it --rm -p 8080:80 --name php-dos-attack-server -v "$PWD"/server:/var/www/html php:5.6-apache
```

Docker will map the port `80` of the webserver to `8080`.
Therefore you can visit your site at `localhost:8080`.

## Run a Hash Collision Attack

You need Python 2.7.
Install the requirements:

```
pip install -r requirements.txt
```

The `attack.py` script will make parallel requests (amount can be specified with `--count`)
to a URL endpoint. It reads collisions from given text file and tries to do a
Hash collision Attack with them. You can set the attack type to either use form fields
or a json map.

Make one request to the webserver running in the docker container.

```
python attack.py http://localhost:8080/index.php collision_keys.txt
```

Make a normal request to compare with the collision attack.

```
python attack.py http://localhost:8080/index.php hashes.txt --no-collide
```

Make 100 requests to a fake JSON API.

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

### Run tests

Run tests for inserting colliding keys into array:

```
php test/array.php collision_keys.txt
```
Run tests for calling `json_decode` for JSON key-value pairs with colliding keys:

```
php test/json_decode.php collision_keys.txt
```
Run tests when `unserializing` an array with colliding keys:

```
php test/unserialize.php collision_keys.txt
```

Run tests when parsing XML with elements name that should collide with each other
into a class with `xml_parse_into_struct`:

```
php test/xml_parse_into_struct.php collision_keys.txt
```

## Plot time difference

You can generate the plot data used for the diagrams by yourself:

```
php plot/array.php collision_keys.txt
```

![json_decode time compared for collisions](/plot/json_decode_time.png)
