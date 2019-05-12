"""
    By: Akshay Sharma, <akshay.sharma09695@gmail.com>
"""
from utils.argument_reader import read_arguments
from utils.moving_average_calculator import MovingAverageCalculator


def aggregate_stats():
    """
        To keep our code readable and organized, I have helper functions/classes to a package name utils.
        The package has helper classes/functions to read/validate the argument passed, mutate timestamps, calculate the moving average
        as well as write the output to a file.
    """

    args = read_arguments()
    source_file = args.input_file
    window_size = args.window_size
    output_file = args.output_file

    moving_avg = MovingAverageCalculator(source_file, output_file, window_size)

    moving_avg.calculate_moving_average()
    moving_avg.write_to_file()


if __name__ == "__main__":
    aggregate_stats()
