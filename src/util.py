import time
import calendar

lines = ["HWD", "LWS", "SSE"]

stations = {
    "HWD": ["HWD", "WVF", "BUG", "HSK", "PRP"],
    "SSE": ["SSE", "SWK", "FSG", "PLD", "AGT", "HOV"],
    "LWS": ["LWS", "PMP", "CBR", "FMR", "MCB", "LRB"]
}

lineTimesFromBrighton = {
    "HWD": [],
    "LWS": [],
    "SSE": []
}

lineTimesToBrighton = {
    "HWD": [[7,24],[8,54],[9,38],[10,14],[11,24],[13,41],[14,29],[16,11],[17,45],[18,45],[19,30],[20,11]],
    "LWS": [],
    "SSE": []
}

def seconds_since_epoch_for_query(myQuery):
    """Calculates and returns seconds since epoch for the beginning of the hour of departure of a rail service"""
    dateTime = "{} {}:00:00".format(myQuery.fromDate, myQuery.fromTime[:2])
    timeStr = time.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
    return calendar.timegm(timeStr)


def is_response_code_valid(response, APIName):
    if response.status_code != 200:
        print(APIName, "call failed.")
        print(str(response.status_code), response.reason)
        return False
    return True


def is_toc_format_valid(code):
    """Validates a TOC code to ensure it is of correct type and length"""
    if isinstance(code, str) and len(code) == 3:
        if code == "BTN":
            return True
        for line in stations.values():
            if code in line:
                return True
        print("Station not on any line in scope.")
        return False
    else:
        print("Station code is in incorrect format.")
        return False
