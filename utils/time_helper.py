"""
    By: Akshay Sharma, <akshay.sharma09695@gmail.com>
"""
import time
from datetime import datetime
from . import system


class TimeHelper:

    @classmethod
    def to_epoch(cls, timestamp, time_format='%Y-%m-%d %H:%M:%S.%f'):
        """
        Convert a given timestamp to epoch time.

        :param timestamp: Date time string
        :param time_format: Date time string. eg: 2018-12-26 18:11:08.509654
        :return: epoch time of the date time string
        """
        try:
            date = datetime.strptime(timestamp, time_format)
            epoch_time = time.mktime(date.timetuple())
            return epoch_time
        except ValueError:
            print("\nError: Incorrect timestamp passed: {0}".format(timestamp))
            system.exit()

    @classmethod
    def convert_epoch_to_minute(cls, epoch_time):
        """
        Class method to convert the epoch time to it's equivalent time in date and minutes.

        :param epoch_time:
        :return: Time in date and minutes
        """
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))

    @classmethod
    def get_minute_from_timestamp(cls, timestamp):
        """
        Helper function to convert the epoch time to minute timestamp.

        :param timestamp: Epoch time to be converted to required date and minutes., eg: 1545828139.0 -> 2018-12-26 18:12:00
        :return: The the converted epoch to minutes
        """
        epoch_time = cls.to_epoch(timestamp)
        # https://docs.python.org/3.6/library/time.html#time.strftime
        return time.strftime('%Y-%m-%d %H:%M', time.localtime(epoch_time))
