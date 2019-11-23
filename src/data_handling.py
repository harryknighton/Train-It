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
    numStations = 0
    reachedStartOfLine = False
    for location in locations:
        if location['location'] in lineEndpoints:
            reachedStartOfLine = not reachedStartOfLine  # Start/Stop considering stations
        elif not reachedStartOfLine:
            continue  # Skip stations until the stations considered in scope of project are reached.
        stationDelay = int(location['actual_ta']) - int(location['gbtt_pta'])
        totalDelay += stationDelay
        numStations += 1
    averageDelay = round(totalDelay / numStations, 1)
    return averageDelay


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
    return delay


def one_hot_encode(row):
    row["HWD Line"] = 1 if row["Line"] == "HWD" else 0
    row["LWS Line"] = 1 if row["Line"] == "LWS" else 0
    row["SSE Line"] = 1 if row["Line"] == "SSE" else 0
    row = row.drop(labels="Line")
    return row


# Data collection
"""
varsToFind = ["Temperature", "Precipitation", "Wind Speed", "Delay"]
lowest = dict.fromkeys(varsToFind, 10000)
highest = dict.fromkeys(varsToFind, -10000)
for month in range(1, 13):
    for day in [1, 10, 20]:
        for time in [[7, 58], [13, 58]]:
            myQ = query.Query("WVF", "BTN", [day, month, 2019], time)
            if myQ.dayType != "WEEKDAY":
                continue
            row = None
            try:
                row = data.get_input_data_for_date(myQ)
            except:
                continue
            for var in varsToFind:
                if row[var] < lowest[var]:
                    lowest[var] = row[var]
                elif row[var] > highest[var]:
                    highest[var] = row[var]

print("Lowest", lowest)
print("Highest", highest)
"""