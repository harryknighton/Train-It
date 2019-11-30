import query
import data_collection as data

"""
    TODO LIST:
"""
myQ = None
try:
    myQ = query.Query("LWS", "BTN", [17, 10, 2019], [14, 48])
except ValueError:
    print("Bad input data for query.")
    quit()

data.get_next_query()

