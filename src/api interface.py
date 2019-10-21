import requests
import json

import query

USER = "harry.knighton18@students.bhasvic.ac.uk"
PW = "HarryKnighton01234!"

def make_request(myQuery):
    ENDPOINT = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
    data = myQuery.to_dict()
    print("Making Request")
    response = requests.post(ENDPOINT, json=data, auth=(USER, PW))
    return response

myQ = None
try:
    myQ = query.Query("HHE", "BTN", [19, 6, 2018], [14, 00])
except ValueError:
    print("Bad input data for query")
myQ.toTime = "1500"

res = make_request(myQ)
if res != 200:
    print(res.status_code)
    print(res.reason)
else:
    jsonResponse = res.json()
    print(jsonResponse["Services"])
    RID = jsonResponse["Services"][0]["serviceAttributesMetrics"]["rids"][0]
    print("Requested RID: " + RID)