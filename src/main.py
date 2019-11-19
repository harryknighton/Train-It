import query
import data_handling as data

"""
    TODO LIST:
    -detail errors
"""
myQ = None
try:
    myQ = query.Query("HWD", "BTN", [4, 6, 2019], [7, 56])
except ValueError:
    print("Bad input data query")
    quit()

try:
    data = data.get_input_data_for_date(myQ)
    print(data)
except RuntimeError as er:
    print("Data retrieval failed.")