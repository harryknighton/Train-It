import time
import calendar


def seconds_since_epoch_for_query(myQuery):
    """Calculates and returns seconds since epoch for the beginning of the hour of departure of a rail service"""
    dateTime = "{} {}:00:00".format(myQuery.fromDate, myQuery.fromTime[:2])
    timeStr = time.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
    return calendar.timegm(timeStr)
