import datetime

class Query:
    def __init__(self, pSource, pDestination, pDate, pTime):
        if self.is_str_param_valid(pSource) and self.is_str_param_valid(pDestination):
            self.source = pSource
            self.destination = pDestination
        else:
            raise ValueError

        if 1 <= pDate[0] <= 31 and 1 <= pDate[1] <= 12 and 2019 <= pDate[2] <= 2021:
            self.fromDate = "{}-{}-{}".format(pDate[2], str(pDate[1]).zfill(2), str(pDate[0]).zfill(0))
            self.toDate = self.fromDate
            self.toDate = self.toDate[0:8] + str(int(self.toDate[-2:]) + 1).zfill(2)
            self.dayType = ""
            self.set_day_type(pDate)
        else:
            raise ValueError

        if 0 <= pTime[0] <= 23 and 0 <= pTime[1] <= 59:
            self.fromTime = str(pTime[0]).zfill(2) + str(pTime[1]).zfill(2)
            self.toTime = "00" if (int(self.fromTime[0:2])) else str(int(self.fromTime[0:2]) + 1).zfill(2)
            self.toTime += self.fromTime[-2:]
        else:
            raise ValueError

    def is_str_param_valid(self, param):
        if isinstance(param, str) and len(param) == 3:
            return True
        else:
            return False

    def set_day_type(self, pDate):
        myDate = datetime.date(pDate[2], pDate[1], pDate[0])
        weekday = myDate.weekday()
        if weekday == 5:
            self.dayType = "SATURDAY"
        elif weekday == 6:
            self.dayType = "SUNDAY"
        else:
            self.dayType = "WEEKDAY"

    def to_params(self):
        params = {}
        params["from_loc"] = self.source
        params["to_loc"] = self.destination
        params["from_time"] = self.fromTime
        params["to_time"] = self.toTime
        params["from_date"] = self.fromDate
        params["to_date"] = self.toDate
        params["days"] = self.dayType
        return params