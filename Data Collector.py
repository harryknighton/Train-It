import datetime

class Query:
    def __init__(self, pSource, pDestination, pDate, pTime):
        if self.is_str_param_valid(pSource) and self.is_str_param_valid(pDestination):
            self.source = pSource
            self.destination = pDestination
        else:
            raise ValueError

        if 1 <= pDate[0] <= 31 and 1 <= pDate[1] <= 12 and 2019 <= pDate[2] <= 2021:
            self.date = "{}-{}-{}".format(pDate[2], str(pDate[1]).zfill(2), str(pDate[0]).zfill(0))
            self.dayType = ""
            self.set_day_type(pDate)
        else:
            raise ValueError

        if 0 <= pTime[0] <= 23 and 0 <= pTime[1] <= 59:
            self.time = str(pTime[0]).zfill(2) + str(pTime[1]).zfill(2)
        else:
            raise ValueError


    def is_str_param_valid(self, param):
        if isinstance(param, str) and len(param) == 3:
            return True
        else:
            return False

    def set_day_type(self, pDate):
        myDate = datetime.date(pDate[0], pDate[1], pDate[2])
        weekday = myDate.weekday()
        if weekday == 5:
            self.dayType = "SATURDAY"
        elif weekday == 6:
            self.dayType = "SUNDAY"
        else:
            self.dayType = "WEEKDAY"

try:
    myQ = Query("HWD", "BTN", [21, 6, 2019], [23, 15])
    print(myQ.destination)
    print(myQ.source)
    print(myQ.date)
    print(myQ.time)
    print(myQ.dayType)
except ValueError:
    print("ValueError was raised")