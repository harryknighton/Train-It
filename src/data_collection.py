import query
import random
import util
import os

import data_handling as data
import errors

_SAVEFILEPATH = "C:\\Users\\hjknighton\\PycharmProjects\\Train-It\\dataset\\dataset.txt"


def get_random_days(month, year):
    days = []
    while True:
        isValid = True
        days = random.sample(range(1, 28), 10)
        for day in days:
            if query.Query.get_day_type([day, month, year]) != "WEEKDAY":
                isValid = False
        if isValid is True:
            break
    return days



def get_two_services(line):
    """Return two random services for a given line"""
    fromBrightonTime = random.choice(util.lineTimesFromBrighton[line])
    services = [{"source": "BTN", "destination": line, "time": fromBrightonTime}]
    toBrightonTime = random.choice(util.lineTimesToBrighton[line])
    services.append({"source": line, "destination": "BTN", "time": toBrightonTime})
    return services


def get_next_query():
    """Get next query to be searched"""
    yearMonths = [[2018, 7, 13], [2019, 1, 7]]
    random.seed()  # Initialise random num generator
    for yearRange in yearMonths:
        year = yearRange[0]
        for month in range(yearRange[1], yearRange[2]):
            days = get_random_days(month, year)
            for day in days:
                for line in util.lines:
                    for service in get_two_services(line):
                        date = [day, month, year]
                        currQ = query.Query(service["source"], service["destination"], date, service["time"])
                        yield currQ


def collect_data():
    """Creates and populates a csv file with train data"""
    if not os.path.exists(_SAVEFILEPATH):
        raise RuntimeError
    with open(_SAVEFILEPATH, 'w', newline="") as saveFile:
        counter = 0  # Only write data to file every 30 queries
        batch = []
        row = None
        skipDate = None
        for myQ in get_next_query():
            if myQ.fromDate == skipDate:
                continue
            print(myQ.to_dict())
            try:
                row = data.get_input_data_for_date(myQ)
                #  Prepare data
                row = data.normalise_values(row)
                row = data.one_hot_encode(row)
                batch.append(row.to_csv(index=False, header=False))
                counter += 1
                #  Write data to csv file
                if counter == 3:
                    saveFile.writelines(batch)
                    counter = 0
                    batch = []
                    break
            except errors.MissingTrainError as e:
                pass
            except errors.MissingWeatherInfoError:
                skipDate = myQ.fromDate  # Skip day as missing info
            except errors.MissingStationDataError:
                print("Missing station data")
            except RuntimeError:
                print("Something went wrong")

        saveFile.write("".join(batch))  # Save any last data


