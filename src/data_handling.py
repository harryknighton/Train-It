import pandas as pd

import api_interface as api

# Combine API calls to produce Database Row

_columnNames = [
    "Line",
    "HHE Line",
    "LWS Line",
    "SSE Line",
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
    lineEndpoints = ["HHE", 'SSE', 'LWS', 'BTN']
    totalDelay = 0
    numStations = 0
    reachedStartOfLine = False
    for location in locations:
        if location['location'] in lineEndpoints:
            reachedStartOfLine = not reachedStartOfLine  # Start/Stop considering stations
        elif not reachedStartOfLine:
            continue  # Skip stations until the stations considered in scope of project are reached.
        stationDelay = 0
        if location['gbtt_pta'] != '' and location['actual_ta'] != '':
            stationDelay = int(location['actual_ta']) - int(location['gbtt_pta'])
            numStations += 1
        elif location['gbtt_ptd'] != '' and location['actual_td'] != '':
            stationDelay = int(location['actual_td']) - int(location['gbtt_ptd'])
            numStations += 1
        else:
            pass
        totalDelay += stationDelay

    averageDelay = round(totalDelay / numStations, 2)
    return averageDelay


def get_input_data_for_date(myQ):
    """Combines and returns data from both APIs in a single database row"""
    weatherInfo = api.get_historic_weather_details(myQ)
    locations = api.get_past_service_details(myQ)
    averageDelay = calculate_average_delay(locations)
    fullInfo = [[
        myQ.line,
        -1,
        -1,  # Placeholder to one-hot-encode line
        -1,
        myQ.isRushHour,
        weatherInfo["temperature"],
        weatherInfo["precipIntensity"],
        weatherInfo["windSpeed"],
        weatherInfo["cloudCover"],
        weatherInfo["visibility"],
        averageDelay
    ]]
    return pd.DataFrame(data=fullInfo, columns=_columnNames)


# Data Preparation
_averageWeatherStats = {
    # [0] for min and [1] for max values
    "Temperature": [-5, 30],
    "Precipitation": [0, 1.5],
    "Wind Speed": [0, 25],
    "Visibility": [0, 10],
    "Delay": [-5, 10]
}


def normalise_values(row):
    for varName, data in _averageWeatherStats.items():
        newValue = row[varName] - data[0]
        newValue /= (data[1] - data[0])  # Divide by range
        row[varName] = newValue
    return row


def decode_delay(encodedDelay):
    data = _averageWeatherStats["Delay"]
    delay = encodedDelay * (data[1] - data[0])
    delay += data[0]
    return round(delay, 2)


def one_hot_encode(row):
    row.at[0, "HHE Line"] = 1 if row.at[0, "Line"] == "HHE" else 0
    row.at[0, "LWS Line"] = 1 if row.at[0, "Line"] == "LWS" else 0
    row.at[0, "SSE Line"] = 1 if row.at[0, "Line"] == "SSE" else 0
    row = row.drop(labels="Line", axis=1)
    return row
