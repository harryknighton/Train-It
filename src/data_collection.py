
import random
import os
import concurrent.futures
from time import sleep

import data_handling as data
import api_interface as api
import util
import query
import errors


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


def get_next_queries():
    """Get next query to be searched"""
    yearMonths = [[2019, 7, 9]]
    random.seed()  # Initialise random num generator
    for yearRange in yearMonths:
        year = yearRange[0]
        for month in range(yearRange[1], yearRange[2]):
            days = get_random_days(month, year)
            for day in days:
                dayQueries = []
                for line in util.lines:
                    for service in get_two_services(line):
                        date = [day, month, year]
                        currQ = query.Query(service["source"], service["destination"], date, service["time"])
                        dayQueries.append(currQ)
                yield dayQueries


def collect_data():
    """Creates and populates a csv file with train data"""
    if not os.path.exists(util.dataSetFilePath):
        raise RuntimeError
    with open(util.dataSetFilePath, 'a', newline="") as saveFile:
        with concurrent.futures.ThreadPoolExecutor(6) as pool:
            for dayQs in get_next_queries():
                print(dayQs[0].to_dict())
                try:
                    weatherInfoForDay = api.get_historic_weather_details(dayQs[0])
                except errors.MissingWeatherInfoError:
                    print("\n")
                    continue  # Skip day

                threads = [None]*len(dayQs)
                records = []
                # Create threads
                for i in range(len(dayQs)):
                    threads[i] = pool.submit(data.get_input_data_for_date, dayQs[i], weatherInfoForDay)
                    sleep(5)  # Wait to avoid 503 error

                # Continue once all threads are complete
                for thread in concurrent.futures.as_completed(threads):
                    record = thread.result()
                    if record.empty:
                        continue
                    else:
                        # Prepare data
                        record = data.normalise_values(record)
                        record = data.one_hot_encode(record)
                        recordStr = record.to_csv(index=False, header=False)
                        records.append(recordStr)

                # Save data
                if records:
                    saveFile.write("".join(records))
                    print("\n")
