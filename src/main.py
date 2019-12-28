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

d = data.load_data(20)

train, test = data.split_data(d, 16)
myNN = nn.NeuralNetwork()
f, l = data.separate_features_and_labels(train[0])
result = myNN.train(f, l)
print(result)
loss = nn.get_loss(result, l)
print(loss)
