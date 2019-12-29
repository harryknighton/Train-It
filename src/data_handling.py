import pandas as pd
import numpy as np
from math import ceil

import api_interface as api
import errors
import util


# Combine API calls to produce Database Row

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

    if numStations == 0:
        raise errors.MissingStationDataError
    averageDelay = round(totalDelay / numStations, 2)
    return averageDelay


def get_input_data_for_date(myQ, weatherInfo=None):
    """Combines and returns data from both APIs in a single database row"""
    if weatherInfo is None:
        try:
            weatherInfo = api.get_historic_weather_details(myQ)
        except errors.MissingWeatherInfoError:
            return pd.DataFrame()
    try:
        locations = api.get_past_service_details(myQ)
    except errors.MissingStationDataError:
        print("Missing station data.")
        return pd.DataFrame()
    except errors.MissingTrainError:
        return pd.DataFrame()
    except RuntimeError:
        print("Something went wrong at runtime.")
        return pd.DataFrame()
    try:
        averageDelay = calculate_average_delay(locations)
    except errors.MissingStationDataError:
        print("No valid station data.")
        return pd.DataFrame()
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

    return pd.DataFrame(data=fullInfo, columns=util.columnNames)


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


# Batch Handling

def load_data(numRows=None):
    data = pd.read_csv(util.dataSetFilePath, names=util.columnNames[1:], nrows=numRows)
    return data.to_numpy()


def split_data(data, batchSize):
    """Splits data into two arrays of batches of a given size"""
    testBatch = data[0]
    trainData = data[1]
    # Split data in 4:1 ratio
    for i in range(2, len(data)):
        if i % 5 != 0:
            trainData = np.column_stack([trainData, data[i]])
        else:
            testBatch = np.column_stack([testBatch, data[i]])

    # Split train data set into batches
    numBatches = ceil(trainData.shape[1] / batchSize)
    trainBatches = np.array_split(trainData, numBatches, axis=1)
    return trainBatches, testBatch


def separate_features_and_labels(data):
    labels = data[-1, :]
    features = np.delete(data, obj=-1, axis=0)
    return features, labels
