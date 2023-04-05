"""
Util functions
"""

import re


def clean_data(data_file_handler):
    """
    Receive the week data string and strip it from blank spaces and ensure that all chars are
    upper case.
    :param data_file_handler: Data file handler
    :return: String
    """

    clean_strings = []
    for week_data in data_file_handler.readlines():
        clean_week_data = week_data.strip()
        clean_week_data = clean_week_data.replace(" ", "")
        clean_week_data = clean_week_data.upper()
        clean_strings.append(clean_week_data)

    return clean_strings


def validate_week_data(week_data: str, pattern: str) -> bool:
    """
    Validate if the week data string comply with the pattern.

    :param week_data: String with week data
    :param pattern: regular expression string
    :return:
    """

    if re.match(pattern, week_data):
        return True
    return False
