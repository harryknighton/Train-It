import requests
import json

import query

myQ = -1
try:
    myQ = query.Query("HHE", "BTN", [19, 6, 2018], [14, 00])
except ValueError:
    print("Bad input data for query")

ENDPOINT = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
USER = "harry.knighton18@students.bhasvic.ac.uk"
PW = "HarryKnighton01234!"

myHeaders = {"content-type": "application/json"}
myQ.toTime = "1500"
data = myQ.to_dict()

print(myHeaders)
print(data)

print("Making Request")
response = requests.post(ENDPOINT, json=data, headers=myHeaders, auth=(USER, PW))
print(response.status_code)
print(response.reason)
if response:
    print(response.json()["Services"])