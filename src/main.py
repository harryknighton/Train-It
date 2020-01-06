import pandas as pd

import query
import data_handling as data
import api_interface as api
import errors
import util
import nn
import optimisation as op

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

# myNN = nn.NeuralNetwork([9, 15, 12, 1], 0.0006)
# d = data.load_data()
# print(op.optimally_train_network(myNN, d, 16))
# nn.train_network(myNN, d, 10, 16, showAll=True)
# print(op.optimise_learn_rate(d, [9, 7, 1], 48))

# op.optimise_parameters(d)