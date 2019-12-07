import datetime

import util

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
        if util.is_toc_format_valid(pSource) and util.is_toc_format_valid(pDestination):
            self.source = pSource
            self.destination = pDestination
            self.line = None
            self.set_service_line()  # Determine and set the line the service runs on
        else:
            print("Invalid TOC code")
            raise ValueError

        # Set to date and from date
        if 1 <= pDate[0] <= 31 and 1 <= pDate[1] <= 12 and 2018 <= pDate[2] <= 2020:  # Arbitrary year range
            self.fromDate = "{}-{}-{}".format(pDate[2], str(pDate[1]).zfill(2), str(pDate[0]).zfill(2))
            self.toDate = self.fromDate
            self.dayType = ""
            self.dayType = self.get_day_type(pDate)
        else:
            print("{} not in acceptable bounds for date.".format(pDate))
            raise ValueError

        # Calculates time 5 minutes after departure time
        if 0 <= pTime[0] <= 23 and 0 <= pTime[1] <= 59:
            self.fromTime = str(pTime[0]).zfill(2) + str(pTime[1]).zfill(2)
            self.toTime = None
            self.set_to_time()
            self.isRushHour = None
            self.set_is_rush_hour()  # Set the isRushHour variable
        else:
            print("{} not in acceptable bounds for time.".format(pTime))
            raise ValueError

    @staticmethod
    def get_day_type(pDate):
        """Works out which day type a date falls on and assigns to self.dayType"""
        myDate = datetime.date(pDate[2], pDate[1], pDate[0])
        weekday = myDate.weekday()
        if weekday == 5:
            return "SATURDAY"
        elif weekday == 6:
            return "SUNDAY"
        else:
            return "WEEKDAY"


    def set_to_time(self):
        """Calculate 5 minutes after the fromTime variable and assigns to toTime"""
        if self.fromTime[2:] < "50":  # Will toTime fall in next hour?
            self.toTime = self.fromTime[:2]
        else:
            self.toTime = str(int(self.fromTime[:2]) + 1).zfill(2)  # zfill used to add leading 0 to time
        self.toTime += str((int(self.fromTime[2:]) + 10) % 60).zfill(2)  # Calculates minutes part of time

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

        for lineName, stationList in util.stations.items():
            if stationToFind in stationList:
                self.line = lineName
                break
        if self.line is None:  # Default = Hayward's Heath
            self.line = "HHE"

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
