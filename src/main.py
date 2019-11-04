import query
import api_interface as api


myQ = None
try:
    #myQ = query.Query("HHE", "BTN", [19, 6, 2018], [14, 11])
    myQ = query.Query("HHE", "BTN", [4, 11, 2019], [21, 36])
except ValueError:
    print("Bad input data for query")


res = api.make_forecast_call()
print(res.status_code)
#for hour in res.json()["daily"]["data"]:
    #print(hour)

print(api.seconds_since_epoch_for_date(myQ))