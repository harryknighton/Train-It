import datetime

import query
import util
import data_handling
import errors
import nn

# myQ = None
# try:
#     myQ = query.Query("BTN", "LWS", [19, 7, 2018], [18, 11])
#     details = data_handling.get_input_data_for_date(myQ)
#     print(details)
# except ValueError:
#     print("Bad input data for query.")
#     quit()
# except errors.MissingTrainError as e:
#     pass
# except errors.MissingStationDataError:
#     print("Missing station data.")
# except RuntimeError:
#     pass

sessionNN = None
# sessionNN = nn.NeuralNetwork([9, 15, 12, 1], 0.0003)

def load_network():
    global sessionNN
    sessionNN = nn.NeuralNetwork([9, 15, 12, 1], 0.0003, initFromFile=True)

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
    today = datetime.date.today()
    if date[2] != 2020 or not 1 <= date[1] <= 12:
        raise ValueError("Invalid date")
    currDay = today.day
    # Date should fall in the next 7 days
    if currDay >= 22 and not (currDay <= date[0] <= 31 or date[0] < (currDay + 7) % 31):
        raise ValueError("Invalid date")
    elif not currDay <= date[0] <= currDay + 7:
        raise ValueError("Invalid date")
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
        details = data_handling.get_input_data_for_future_query(userQuery)
    except (RuntimeError, errors.MissingWeatherInfoError):
        return False, "Something went wrong collecting data"
    # Prepare data
    details = data_handling.normalise_values(details, containsDelay=False)
    details = data_handling.one_hot_encode(details)
    prediction = sessionNN.make_prediction(details.T)
    return True, prediction

# testData = ["HHE", "BTN", [8, 1, 2020], "19:30"]
#
# print(process_request(*testData))
load_network()
