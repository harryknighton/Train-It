import requests
import time
import calendar

# Functions to access the HSP API
_USER = "harry.knighton18@students.bhasvic.ac.uk"
_PW = "HarryKnighton01234!"


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


def get_past_service_details(myQuery):
    res = get_metrics(myQuery)
    if res.status_code != 200:
        print("HSP Metrics call failed:")
        print(str(res.status_code), res.reason)
        raise RuntimeError
    RID = res.json()["Services"][0]["serviceAttributesMetrics"]["rids"][0]
    details = get_details(RID)
    if details.status_code != 200:
        print("HSP Details call failed:")
        print(str(details.status_code), details.reason)
        raise RuntimeError
    for loc in details.json()["serviceAttributesDetails"]["locations"]:
        print(loc)


# Dark Sky API
_API_KEY = "d7a272491dc6f6bdfc09b22cdb96c674"
_LAT = "50.924675"
_LONG = "-0.146098"
_UNITS = "units=uk2"


def make_historic_details_call(myQuery):
    excludes = "exclude=minutely,hourly,daily,alerts"
    time = "{}T{}:00:00".format(myQuery.fromDate, myQuery.fromTime[:2])
    URL = "https://api.darksky.net/forecast/{}/{},{},{}?{}&{}".format(_API_KEY, _LAT, _LONG, time, excludes, _UNITS)
    res = requests.get(URL)
    return res


def make_forecast_call():
    excludes = "exclude=currently,minutely,hourly,alerts,flags"
    URL = "https://api.darksky.net/forecast/{}/{},{}?{}&{}".format(_API_KEY, _LAT, _LONG, excludes, _UNITS)
    res = requests.get(URL)
    return res


def get_historic_weather_details(myQuery):
    res = make_historic_details_call(myQuery)
    if res.status_code != 200:
        print("Dark Sky API call failed:")
        print(str(res.status_code), res.reason)
        raise RuntimeError
    else:
        info = res.json()['currently']
        usefulInfo = {}
        wantedProperties = ["temperature", "humidity", "windSpeed", "cloudCover", "visibility"]
        for key in wantedProperties:
            if key in info:
                usefulInfo[key] = info[key]
            else:
                print("Missing " + key + " attribute from Dark Sky response.")
        return usefulInfo


def get_forecast_info(dateOfTravel, hourOfTravel):
    """Handles request for API info, and extracts data from response"""


def seconds_since_epoch_for_date(myQuery):
    """Calculates and returns seconds since epoch for the beginning of a specified hour"""
    dateTime = "{} {}:00:00".format(myQuery.fromDate, myQuery.fromTime[:2])
    timeStr = time.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
    return calendar.timegm(timeStr)
