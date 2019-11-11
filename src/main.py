import query
import api_interface as api


myQ = None
try:
    #myQ = query.Query("HHE", "BTN", [19, 6, 2018], [14, 11])
    myQ = query.Query("HHE", "BTN", [10, 11, 2019], [14, 36])
except ValueError:
    print("Bad input data for query")


data = api.get_historic_weather_details(myQ)
for key, value in data.items():
    print("{}: {}".format(key, value))

