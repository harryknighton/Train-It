import requests
import util
import errors

# Functions to access the HSP API

# Access details
_USER = "harry.knighton18@students.bhasvic.ac.uk"
_PW = "HarryKnighton01234!"


def get_metrics(myQuery):
    """Returns data containing the RID of a desired rail service."""
    ENDPOINT = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
    data = myQuery.to_dict()
    response = requests.post(ENDPOINT, json=data, auth=(_USER, _PW))
    return response


def get_details(rid):
    """Returns information about a specific rail service, identified by it's RID."""
    ENDPOINT = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
    data = {"rid": rid}
    response = requests.post(ENDPOINT, json=data, auth=(_USER, _PW))
    return response


def get_past_service_details(myQuery):
    """Handles making calls to both HSP APIs, including validating responses, and returns the data acquired."""
    res = get_metrics(myQuery)
    if not util.is_response_code_valid(res, "HSP Metrics"):
        raise RuntimeError
    if not res.json()["Services"]:
        print("RID could not be acquired for service.")
        raise errors.MissingTrainError
    RID = res.json()["Services"][0]["serviceAttributesMetrics"]["rids"][0]  # path of RID in JSON response.

    details = get_details(RID)
    if not util.is_response_code_valid(details, "HSP Details"):
        raise RuntimeError
    locations = details.json()["serviceAttributesDetails"]["locations"]  # Extract details of service
    numMissing = 0
    for i in range(2, len(locations)):  # Iterate through intermediate stations
        if locations[-i]["actual_td"] == '':
            numMissing += 1
    if numMissing / len(locations) > 0.3:
        raise errors.MissingStationDataError
    return locations


# Dark Sky API

_API_KEY = "d7a272491dc6f6bdfc09b22cdb96c674"

# Latitude and Longitude of Hassocks Train Station
_LAT = "50.924675"
_LONG = "-0.146098"
_UNITS = "units=uk2"

# Properties to extract from API response
WeatherProperties = ["temperature", "precipIntensity", "windSpeed", "cloudCover", "visibility"]


def extract_useful_weather_data(data):
    wantedAttributes = ["temperature", "precipIntensity", "windSpeed", "cloudCover", "visibility"]
    wantedData = {}
    for key in wantedAttributes:
        if key in data:
            wantedData[key] = data[key]
        elif key == "precipIntensity":
            # If precipIntensity not found, then precipitation was 0 on that day.
            wantedData[key] = 0
        else:
            print("Missing " + key + " attribute from Dark Sky response.")
            raise errors.MissingWeatherInfoError
    return wantedData


def make_historic_weather_call(myQuery):
    """Returns weather details of a specified date in the past."""
    excludes = "exclude=minutely,hourly,daily,alerts"
    time = "{}T{}:00:00".format(myQuery.fromDate, myQuery.fromTime[:2])
    URL = "https://api.darksky.net/forecast/{}/{},{},{}?{}&{}".format(_API_KEY, _LAT, _LONG, time, excludes, _UNITS)
    res = requests.get(URL)
    return res


def make_forecast_call():
    """Returns weather details for the next 7 days."""
    excludes = "exclude=currently,minutely,daily,alerts,flags"
    extends = "extend=hourly"
    URL = "https://api.darksky.net/forecast/{}/{},{}?{}&{}&{}".format(_API_KEY, _LAT, _LONG, excludes, extends,  _UNITS)
    res = requests.get(URL)
    return res


def get_historic_weather_details(myQuery):
    """Validates and extracts useful information from Time Machine API response"""
    res = make_historic_weather_call(myQuery)
    if not util.is_response_code_valid(res, "Dark Sky Time Machine"):
        raise RuntimeError
    else:
        info = res.json()["currently"]
        return extract_useful_weather_data(info)


def get_forecast_info(myQ):
    """Handles request for API info, and extracts data from response"""
    res = make_forecast_call()
    if not util.is_response_code_valid(res, "Dark Sky Forecast"):
        raise RuntimeError
    else:
        data = res.json()["hourly"]["data"]
        targetTime = util.seconds_since_epoch_for_query(myQ)
        targetData = -1
        for hour in data:
            if hour["time"] == targetTime:
                targetData = hour
                break
        return extract_useful_weather_data(targetData), targetData["summary"]
