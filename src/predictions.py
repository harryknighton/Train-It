import datetime
import numpy

import query
import util
import data_handling
import errors
import nn
import optimisation

sessionNN = None


def load_network():
    global sessionNN
    sessionNN = nn.NeuralNetwork([9, 12, 6, 1], 0.0003, initFromFile=True)


def prepare_form_data(src, dest, time):
    """Cleans and prepares form input for use in program"""
    src = src.strip().upper()
    dest = dest.strip().upper()
    # Convert time to list form
    listTime = [int(time[:2]), int(time[-2:])]
    return src, dest, listTime


def validate_form_data(src, dest, date, time):
    """Check if all form input is valid and query can be made"""
    if not util.is_toc_format_valid(src) or not util.is_toc_format_valid(dest):
        raise ValueError("Invalid station code")
    now = datetime.datetime.now()
    currDay = now.day
    currTime = [now.hour, now.minute]
    if date[2] != 2020 or not 1 <= date[1] <= 12:
        raise ValueError("Invalid date")

    # Date should fall in the next 7 days
    if currDay >= 22 and not (currDay <= date[0] <= 31 or date[0] < (currDay + 7) % 31):
        raise ValueError("Invalid date")
    elif not currDay <= date[0] <= currDay + 7:
        raise ValueError("Invalid date")
    # Check date doesn't fall in the past
    if date[0] == currDay:
        if time[0] < currTime[0]:
            raise ValueError("Journey was in the past")
        elif time[0] == currTime[0]:
            if time[1] < currTime[1]:
                raise ValueError("Journey was in the past")
    elif date[0] < currDay:
        raise ValueError("Journey was in the past")

    if not(0 <= time[0] < 24 and 0 <= time[1] < 60):
        raise ValueError("Invalid time")
    return True


def process_request(src, dest, date, time):
    """Takes form data and returns prediction or error message
        :returns (error flag, prediction or error message)
    """
    src, dest, time = prepare_form_data(src, dest, time)
    try:
        validate_form_data(src, dest, date, time)
        userQuery = query.Query(src, dest, date, time)
    except ValueError as e:
        return False, str(e)
    try:
        details, weatherSummary = data_handling.get_input_data_for_future_query(userQuery)
    except (RuntimeError, errors.MissingWeatherInfoError):
        return False, "Something went wrong collecting data"
    # Prepare data
    details = data_handling.normalise_values(details, containsDelay=False)
    details = data_handling.one_hot_encode(details)
    prediction = sessionNN.make_prediction(details.T)
    return True, (prediction, weatherSummary)
