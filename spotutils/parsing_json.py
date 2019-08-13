#!/usr/bin/env python3.5

import json
from pprint import pprint as pp
import os

def base(path: str):
	return path.split("/")[len(path.split("/"))-1]
def get_ids(playlist_link: str):
	with open(playlist_link) as fi:
		content = json.loads(fi.read())
	return [base(element['track']['href']) for element in content['items']]
def combine(manifest: list):
	return list(set().union(*manifest))

first = get_ids("example.json")
second = get_ids("example_two.json")
combined = combine([first, second])
print("Amount of songs in first: {}".format(len(first)))
print("Amount of songs in second: {}".format(len(second)))
print("Total amount, including duplicates: {}".format(len(first)+len(second)))
print("Amount of songs in combined, without duplicates: {}".format(len(combined)))
print(combined)
