import os
import json
import string
import secrets
from random_username.generate import generate_username

ABI = []
CONTRACT_ADDRESS = ""
ADDRESSES = []
PRIVATE_KEYS = {}
USERS = []

with open(os.environ.get('BUILD'), 'r') as build_file:
    build = json.load(build_file)
    ABI = build["abi"]
    CONTRACT_ADDRESS = build['networks'][list(build['networks'].keys())[0]]['address']

with open(os.environ.get('ACCOUNTS'), 'r') as addresses_file:
    addresses = json.load(addresses_file)

    ADDRESSES = list(addresses['addresses'].keys())
    PRIVATE_KEYS = addresses['private_keys']

def _generate_password(length: int):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    
    return password

USERS = {username: {"password": _generate_password(10)} for username in generate_username(len(ADDRESSES))}

with open(os.path.join(os.environ.get("DB_DIR"), "db.json"), "w") as db_file:
    json.dump(USERS, fp=db_file, indent=4)