class CancelledTrainError(Exception):
    def __init__(self, source, time, date):
        self.source = source
        self.time = time
        self.date = date

