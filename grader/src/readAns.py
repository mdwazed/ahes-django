import json
import os
import sys

fileName = os.path.join(os.pardir, 'studentAns.json')

with open(fileName, 'r') as file:
	configData = json.load(file)

print(configData)