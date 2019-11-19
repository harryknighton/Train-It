import pandas as pd

import api_interface as api

# Combine API calls to produce Database Row

_columnNames = [
    "Line",
    "isPeakTime",
    "Temperature",
    "Precipitation",
    "Wind Speed",
    "Cloud Cover",
    "Visibility",
    "Delay"
]

def calculate_average_delay(locations):
    """Calculates and returns the average delay of a rail service"""
    lineEndpoints = ["HWD", 'SSE', 'LWS', 'BTN']
    totalDelay = 0
    reachedStartOfLine = False
    for location in locations:
        if location['location'] in lineEndpoints:
            reachedStartOfLine = not reachedStartOfLine  # Start/Stop considering stations
        elif not reachedStartOfLine:
            continue  # Skip stations until the stations considered in scope of project are reached.
        stationDelay = int(location['actual_ta']) - int(location['gbtt_pta'])
        totalDelay += stationDelay
    return round(totalDelay / (len(locations)-1), 1)  # Return mean average of delays


def get_input_data_for_date(myQ):
    """Combines and returns data from both APIs in a single database row"""
    trainInfo = api.get_past_service_details(myQ)
    averageDelay = calculate_average_delay(trainInfo['locations'])
    weatherInfo = api.get_historic_weather_details(myQ)
    fullInfo = [
        myQ.line,
        myQ.isRushHour,
        weatherInfo["temperature"],
        weatherInfo["precipIntensity"],
        weatherInfo["windSpeed"],
        weatherInfo["cloudCover"],
        weatherInfo["visibility"],
        averageDelay
    ]
    return pd.Series(fullInfo, index=_columnNames)
def normalise_values():
    pass