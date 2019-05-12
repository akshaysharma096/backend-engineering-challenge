"""
    By: Akshay Sharma, <akshay.sharma09695@gmail.com>
"""

from .time_helper import TimeHelper
from . import json
from queue import Queue
from . import system
from collections import deque


class MovingAverageCalculator:
    """

        Basic Idea to solve this problem is to group the events, by on the basis of the minute they happened.
        We keep track of the window size by by keeping an internal queue.
        Once the size grows more than the window size, the internal queue pops from front to update the moving average.
    """

    def __init__(self, source_file, output_file, window_size):
        self.source_file = source_file
        self.output_file = output_file
        self.stream_collection = {}
        self.input_stream = []
        self.output_stream = deque()
        self.window_size = window_size
        self.moving_avg_queue = Queue()

    def _parse_stream(self):
        """
        Helper function which groups the events by the minute they occurred, which done using the epoch time of the minute.
        :return:
        """
        self._build_stream()

        for event in self.input_stream:
            if not all(key in event for key in ('event_name', 'duration')):
                # If any of key does not exist, skip.
                continue

            if event['event_name'] != 'translation_delivered':
                # By pass those events, which do not match the required event type
                continue

            minutes_passed = TimeHelper.get_minute_from_timestamp(event['timestamp'])
            epoch_time = TimeHelper.to_epoch(minutes_passed, time_format="%Y-%m-%d %H:%M")

            if epoch_time not in self.stream_collection:
                self.stream_collection[epoch_time] = {'duration_count': 0, 'elements': 0}
            self.stream_collection[epoch_time]['duration_count'] += event['duration']
            self.stream_collection[epoch_time]['elements'] += 1

        # If all the events are invalid, we need to do nothing.
        if len(self.stream_collection.keys()) > 0:
            self.min_time_stamp = min(self.stream_collection.keys())
            self.max_time_stamp = max(self.stream_collection.keys())
        else:
            self.max_time_stamp = self.min_time_stamp = None

    def _build_stream(self):
        """
        Helper function to load the JSON data from the input file.
        :return:
        """
        try:
            with open(self.source_file) as file:
                for line in file:
                    event = json.loads(line)
                    self.input_stream.append(event)
        except json.decoder.JSONDecodeError:
            print("\nError: Input file {0}, is not a valid JSON file.".format(self.source_file))
            system.exit()

    def calculate_moving_average(self):
        """
        Function to calculate the moving average of the stream of events, using an internal queue

        :return: None
        """
        self._parse_stream()

        initial_timestamp, last_timestamp = self.min_time_stamp, self.max_time_stamp

        if not initial_timestamp or not last_timestamp:
            return

        minutes_delta = int((last_timestamp - initial_timestamp) / 60) + 2

        total_event_count = 0
        total_duration_count = 0

        for i in range(minutes_delta):
            time_window = initial_timestamp + i * 60

            current_event_count = 0
            current_duration_count = 0

            if self.moving_avg_queue.qsize() == self.window_size + 1:
                # If the queue size is greater than what is required
                # Remove the first element from the queue and update the total count and duration of events.
                previous_duration, previous_events = self.moving_avg_queue.get()
                total_event_count -= previous_events
                total_duration_count -= previous_duration

            timestamp_by_minute = TimeHelper.convert_epoch_to_minute(time_window)

            average_delivery_time = self._find_avg_delivery_time(total_event_count, total_duration_count)
            self._write_to_output_stream(timestamp_by_minute, average_delivery_time)

            if time_window in self.stream_collection:
                # Calculate the current duration of events and the number of events in this time window.
                current_event_count = self.stream_collection[time_window]['elements']
                current_duration_count = self.stream_collection[time_window]['duration_count']

            # Update the total duration and total count
            total_event_count += current_event_count
            total_duration_count += current_duration_count

            # Dump it into the queue for later usage.
            self.moving_avg_queue.put((current_duration_count, current_event_count))

    def _write_to_output_stream(self, date, moving_avg):
        """
        Helper function that writes the moving average to our output stream

        :param date: Timestamp
        :param moving_avg: Moving average value for that timestamp
        :return: None
        """
        self.output_stream.append({'date': date, 'average_delivery_time': moving_avg})

    def write_to_file(self):
        """
        Function to write our output stream to the required outfile.
        :return:
        """
        with open(self.output_file, 'w') as file:
            for average_value in self.output_stream:
                json_str = json.dumps(average_value)
                file.writelines(json_str + "\n")

    @staticmethod
    def _find_avg_delivery_time(total_number_of_events, total_number_of_durations):
        """
        Helper function to find the delivery time given set of events and the total duration
        """
        if total_number_of_events > 0:
            if total_number_of_durations % total_number_of_events == 0:
                return total_number_of_durations // total_number_of_events
            else:
                return total_number_of_durations / total_number_of_events
        else:
            return 0
