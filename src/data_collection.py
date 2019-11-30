import query
import random
import util

def get_two_services(line):
    """Return two random services for a given line"""
    fromBrightonTime = random.choice(util.lineTimesFromBrighton[line])
    services = [{"source": "BTN", "destination": line, "time": fromBrightonTime}]
    toBrightonTime = random.choice(util.lineTimesToBrighton[line])
    services.append({"source": "BTN", "destination": line, "time": toBrightonTime})
    return services


def get_next_query():
    yearMonths = [[2018, 7, 13], [2019, 1, 7]]
    random.seed()
    for yearRange in yearMonths:
        year = yearMonths[0]
        for month in range(yearRange[1], yearRange[2]):
            days = random.sample(range(1, 28), 10)  # Choose 10 random days
            for day in days:
                for line in util.lines:
                    for service in get_two_services(line):
                        date = [day, month, year]
                        currQ = query.Query(service["source"], service["destination"], date, service["time"])
                        yield currQ






def prepare_data():
    pass


def collect_data():
    pass