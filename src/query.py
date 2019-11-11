import datetime

class Query:
    """Contains all the data required to obtain weather and rail service information on a specified day"""
    def __init__(self, pSource, pDestination, pDate, pTime):
        """Validates and initialises all variables needed for use with API

        :param pSource: Source station
        :param pDestination: Destination station
        :param pDate: Date of departure
        :param pTime: Time of departure
        :raises ValueError: Raised if an invalid parameter value is passed in
        """
        if self.is_toc_format_valid(pSource) and self.is_toc_format_valid(pDestination):
            self.source = pSource
            self.destination = pDestination
        else:
            raise ValueError

        if 1 <= pDate[0] <= 31 and 1 <= pDate[1] <= 12 and 2018 <= pDate[2] <= 2020:  # Arbitrary year range
            self.fromDate = "{}-{}-{}".format(pDate[2], str(pDate[1]).zfill(2), str(pDate[0]).zfill(2))
            self.toDate = self.fromDate
            self.dayType = ""
            self.set_day_type(pDate)
        else:
            raise ValueError

        # Calculates time 5 minutes after departure time
        if 0 <= pTime[0] <= 23 and 0 <= pTime[1] <= 59:
            self.fromTime = str(pTime[0]).zfill(2) + str(pTime[1]).zfill(2)
            if self.fromTime[2:] < "55":
                self.toTime = self.fromTime[:2]
            else:
                self.toTime = str(int(self.fromTime[:2]) + 1).zfill(2)
            self.toTime += str(int(self.fromTime[2:]) + 5 % 60).zfill(2)
        else:
            raise ValueError

    def is_toc_format_valid(self, param):
        """Validates a TOC code to ensure it is of correct type and length"""
        if isinstance(param, str) and len(param) == 3:
            return True
        else:
            return False

    def set_day_type(self, pDate):
        """Works out which day type a date falls on and assigns to self.dayType"""
        myDate = datetime.date(pDate[2], pDate[1], pDate[0])
        weekday = myDate.weekday()
        if weekday == 5:
            self.dayType = "SATURDAY"
        elif weekday == 6:
            self.dayType = "SUNDAY"
        else:
            self.dayType = "WEEKDAY"

    def to_dict(self):
        """Combines all query information into a dictionary, suitable to be passed to an API"""
        params = {}
        params["from_loc"] = self.source
        params["to_loc"] = self.destination
        params["from_time"] = self.fromTime
        params["to_time"] = self.toTime
        params["from_date"] = self.fromDate
        params["to_date"] = self.toDate
        params["days"] = self.dayType
        return params
