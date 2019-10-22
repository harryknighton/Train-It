import query
import api_interface as api

myQ = None
try:
    myQ = query.Query("HHE", "BTN", [19, 6, 2018], [14, 11])
except ValueError:
    print("Bad input data for query")

res = api.get_metrics(myQ)
if res.status_code != 200:
    print(res.status_code)
    print(res.reason)
else:
    jsonResponse = res.json()
    RID = jsonResponse["Services"][0]["serviceAttributesMetrics"]["rids"][0]
    print("Requested RID: " + RID)
    details = api.get_details(RID)
    for loc in details.json()["serviceAttributesDetails"]["locations"]:
        print(loc)