import requests
import json

import query

try:
    myQ = query.Query("HWD", "BTN", [21, 6, 2019], [23, 15])
    params = myQ.to_params()
except ValueError:
    print("Bad input data for query")

ENDPOINT = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"

headers = {}
headers["Content-Type"] = "application/json"
headers["Authorization"] = "Basic{}"

