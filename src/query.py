import datetime

_stations = {
    "HWD": ["HWD", "WVF", "BUG", "HSK", "PRP"],
    "SSE": ["SSE", "SWK", "FSG", "PLD", "AGT", "HOV"],
    "LWS": ["LWS", "PMP", "CBR", "FMR", "MCB", "LRB"]
}

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

        # Set source and destination stations
        if self.is_toc_format_valid(pSource) and self.is_toc_format_valid(pDestination):
            self.source = pSource
            self.destination = pDestination
            self.line = None
            self.set_service_line() # Determine and set the line the service runs on
        else:
            raise ValueError

        # Set to date and from date
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
            self.toTime = None
            self.set_to_time()
            self.isRushHour = None
            self.set_is_rush_hour()  # Set the isRushHour variable
        else:
            raise ValueError

    def is_toc_format_valid(self, code):
        """Validates a TOC code to ensure it is of correct type and length"""
        if isinstance(code, str) and len(code) == 3:
            if code == "BTN":
                return True
            for line in _stations.values():
                if code in line:
                    return True
            print("Station not on any line in scope.")
            return False
        else:
            print("Station code is in incorrect format.")
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


    def set_to_time(self):
        """Calculate 5 minutes after the fromTime variable and assigns to toTime"""
        if self.fromTime[2:] < "55":  # Will toTime fall in next hour?
            self.toTime = self.fromTime[:2]
        else:
            self.toTime = str(int(self.fromTime[:2]) + 1).zfill(2)  # zfill used to add leading 0 to time
        self.toTime += str(int(self.fromTime[2:]) + 5 % 60).zfill(2)  # Calculates minutes part of time

    def set_is_rush_hour(self):
        """Checks whether the service is running during peak times"""
        intTime = int(self.fromTime)
        if 630 <= intTime < 930 or 1600 <= intTime < 1900:
            self.isRushHour = True
        else:
            self.isRushHour = False

    def set_service_line(self):
        """Determines which line the service runs on and sets variable 'line'"""
        # Brighton is on every line, so need to check the destination
        if self.source == "BTN":
            stationToFind = self.destination
        else:  # Otherwise check which line source resides on
            stationToFind = self.source

        for lineName, stationList in _stations.items():
            if stationToFind in stationList:
                self.line = lineName
                break
        if self.line is None:  # Default = Hayward's Heath
            self.line = "HWD"

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
