import pandas as pd

import query
import data_handling as data
import api_interface as api
import errors
import util
import nn

"""
    TODO LIST:
"""

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

myNN = nn.NeuralNetwork()
d = data.load_data()
nn.train_network(myNN, d, 100, 48, showAll=True)
