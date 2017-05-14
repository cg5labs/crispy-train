#!/usr/bin/python

import json

with open('donut.json') as json_data:
    d = json.load(json_data)
    print(d)
    print("==> parsing object")
    print(d['topping'])

json_string = '{"first_name": "Guido", "last_name":"Rossum"}'

parsed_json = json.loads(json_string)

print(parsed_json['first_name'])

# convert dict to JSON

d = {
    'first_name': 'Guido',
    'second_name': 'Rossum',
    'titles': ['BDFL', 'Developer'],
}

print(json.dumps(d))

