"""
    By: Akshay Sharma, <akshay.sharma09695@gmail.com>
"""

from argparse import ArgumentParser
from pathlib import Path
from . import system


def read_arguments():
    """
    Function to read arguments passed in our application
    :return: Arguments
    """
    argument_parser = ArgumentParser(description='Moving Average Aggregator, UnBabel challenge')

    argument_parser.add_argument('-i', '--input_file',
                                 help='Input  File', required=True)

    argument_parser.add_argument('-w', '--window_size', type=int,
                                 help='Window Size', required=True)

    argument_parser.add_argument('-o', '--output_file',
                                 help='Output File', required=True)

    arguments = argument_parser.parse_args()

    return validate_arguments(arguments)


def validate_arguments(arguments):
    """
    Helper function to validate the arguments passed in our application
    :param arguments: A
    :return:
    """
    source_file = arguments.input_file
    window_size = arguments.window_size

    file = Path(source_file)
    if not file.is_file():
        print("\nError: Source file {0}, file not found".format(source_file))
        system.exit(1)

    if window_size < 1:
        print("\nError: Window size should be at least greater than or equal to 1.")
        system.exit(1)

    return arguments
