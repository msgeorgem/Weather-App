from datetime import datetime


class TimestampConverter:
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def to_localdatetime(self):
        # Convert the timestamp to a datetime object
        dt_object = datetime.fromtimestamp(self.timestamp)
        
        # Format the datetime object as a string
        localdatetime = dt_object.strftime("%H:%M:%S")
        # localdatetime = dt_object.strftime("%Y-%m-%d %H:%M:%S")
        
        return localdatetime
    



