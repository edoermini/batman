import json
import os
import time

BUILD_FILE = os.environ.get("BUILD")

while True:
    if not os.path.isfile(BUILD_FILE):
        time.sleep(1)
        continue

    with open(BUILD_FILE, 'r') as build:
        if not json.load(build)['networks']:
            time.sleep(1)
            continue
    
    break