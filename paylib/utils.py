"""
Util functions
"""

import re

from .config import message_strings, week_string_pattern


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


def read_week_data(
    data_file_handler,
    clean_func=clean_data,
    validate_func=validate_week_data,
    error_message=message_strings["format_error_message"],
    string_pattern=week_string_pattern,
):
    """
    Read each line in the data file, clean and validate. If valid add to the return list,
    if not include an error message.

    :param data_file_handler: file handler
    :param clean_func: clean function
    :param validate_func: validation function
    :param error_message: Error message
    :param string_pattern: Pattern to evaluate if a string is valid
    :return: list of dicts with two keys, valid and text
    """

    # Clean data file strings
    data_strings = clean_func(data_file_handler)

    result_dicts = []

    # If a string is valid, append it to the result, if not, append an error message
    for count, data_string in enumerate(data_strings, 1):
        if validate_func(data_string, string_pattern):
            result_dicts.append({"valid": True, "text": data_string})
        else:
            result_dicts.append(
                {
                    "valid": False,
                    "text": error_message.format(count, data_string),
                }
            )

    return result_dicts
