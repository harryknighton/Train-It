import time
import calendar

dataSetFilePath = "C:\\Users\\hjknighton\\PycharmProjects\\Train-It\\saves\\dataset.txt"
paramFilePath = "C:\\Users\\hjknighton\\PycharmProjects\\Train-It\\saves\\parameters.txt"

columnNames = [
    "Line",
    "HHE Line",
    "LWS Line",
    "SSE Line",
    "isPeakTime",
    "Temperature",
    "Precipitation",
    "Wind Speed",
    "Cloud Cover",
    "Visibility",
    "Delay"
]

lines = ["HHE", "LWS", "SSE"]

stations = {
    "HHE": ["HHE", "WVF", "BUG", "HSK", "PRP"],
    "SSE": ["SSE", "SWK", "FSG", "PLD", "AGT", "HOV"],
    "LWS": ["LWS", "PMP", "CBR", "FMR", "MCB", "LRB"]
}

lineTimesFromBrighton = {
    "HHE": [[7,37],[8,40],[9,28],[10,9],[11,28],[12,39],[13,58],[15,3],[16,9],[17,33],[18,28],[20,3]],
    "LWS": [[7,31],[8,41],[9,51],[11,1],[12,31],[13,21],[14,51],[16,1],[17,21],[18,11],[19,41]],
    "SSE": [[7,20],[8,32],[9,51],[10,39],[12,2],[13,9],[14,39],[15,51],[17,2],[18,10],[19,22],[20,10]]
}

lineTimesToBrighton = {
    "HHE": [[7,24],[8,54],[9,38],[10,14],[11,24],[13,41],[14,29],[16,11],[17,45],[18,45],[19,30],[20,11]],
    "LWS": [[7,43],[8,33],[9,43],[10,13],[10,53],[12,23],[13,43],[15,3],[16,13],[18,3],[19,14],[20,39]],
    "SSE": [[7,27],[8,20],[9,5],[9,56],[10,43],[12,26],[13,12],[14,5],[15,53],[17,5],[18,35],[19,56]]
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


