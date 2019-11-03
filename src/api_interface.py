import requests


#Functions to access the HSP API
USER = "harry.knighton18@students.bhasvic.ac.uk"
PW = "HarryKnighton01234!"

def get_metrics(myQuery):
    ENDPOINT = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
    data = myQuery.to_dict()
    print("Making Request")
    response = requests.post(ENDPOINT, json=data, auth=(USER, PW))
    return response

def get_details(rid):
    ENDPOINT = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
    data = {"rid": rid}
    response = requests.post(ENDPOINT, json=data, auth=(USER, PW))
    return response

#Dark Sky API
def get_historic_weather_etails(myQuery):
    APIKEY = "d7a272491dc6f6bdfc09b22cdb96c674"
    LAT = "50.924675"
    LONG = "-0.146098"
    TIME = "{}T{}:00:00".format(myQuery.fromDate, myQuery.fromTime[:2])
    EXCLUDES = "exclude=minutely,hourly,daily,alerts"
    UNITS = "units=uk2"
    URL = "https://api.darksky.net/forecast/{}/{},{},{}?{}&{}".format(APIKEY, LAT, LONG, TIME, EXCLUDES, UNITS)
    res = requests.get(URL)
    return res
