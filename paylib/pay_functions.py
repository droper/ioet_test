"""
Payment functions
"""

from datetime import datetime, timedelta
from collections import OrderedDict

from .config import message_strings, week_string_pattern
from .utils import clean_data, validate_week_data


def read_week_data(
    data_file_handler, clean_func=clean_data, validate_func=validate_week_data
):
    """
    Read each line in the data file, clean and validate. If valid add to the return list,
    if not include an error message.

    :param data_file_handler: file handler
    :param clean_func: clean function
    :param validate_func: validation function
    :return: list of dicts with two keys, valid and text
    """

    # Clean data file strings
    data_strings = clean_func(data_file_handler)

    result_dicts = []

    # If a string is valid, append it to the result, if not, append an error message
    for count, data_string in enumerate(data_strings, 1):
        if validate_func(data_string, week_string_pattern):
            result_dicts.append({"valid": True, "text": data_string})
        else:
            result_dicts.append(
                {
                    "valid": False,
                    "text": message_strings["format_error_message"].format(
                        count, data_string
                    ),
                }
            )

    return result_dicts


def worker_pay(worker_week_string: str) -> str:
    """
    Receives a string with the worker name and week hours worked.

    :param worker_week_string: Data string with the format 'NAME=WD##:##-##:##,WD##:##-##:##' where WD is the
                 abbreviation of the day.
    :return: A string with the amount of dollars to pay for each worker.
    """

    parts = worker_week_string.split("=")
    name = parts[0]
    week_hours = parts[1]

    return message_strings["amount_message"].format(name, week_pay(week_hours))


def week_pay(week_data: str) -> float:
    """
    Receives a week worked hours data and returns the amount of dollars to pay. For a day the amount of
    hours in each interval is calculated and used to multiply it for the hour salary.

    :param week_data: Data string with the format 'WD##:##-##:##,WD##:##-##:##' where WD is the abbreviation
                 of the day.
    :return: The amount of dollars to pay for each worker.
    """

    # Split the data string into the day hours intervals
    week_hours = week_data.split(",")

    result = 0
    # Loop over each day in the data string
    for day_hours in week_hours:
        result += day_pay(day_hours)

    return round(result, 2)


def day_pay(day_data: str) -> float:
    """
    Receives a working day data and returns the payment for that day.

    :param day_data: string in the format WD##:##, where WD is the abbreviation of the week day
    :return: a float with the amount of dollars for the day
    """

    WD = "wd"
    WE = "we"

    # Days dictionary, each day has is type
    days = {
        "MO": WD,
        "TU": WD,
        "WE": WD,
        "TH": WD,
        "FR": WD,
        "SA": WE,
        "SU": WE,
    }

    hf = "%H:%M"

    # The intervals that divide a day
    day_intervals = {
        "n": {
            "begin": datetime.strptime("00:00", hf),
            "end": datetime.strptime("9:00", hf),
        },
        "d": {
            "begin": datetime.strptime("9:00", hf),
            "end": datetime.strptime("18:00", hf),
        },
        "e": {
            "begin": datetime.strptime("18:00", hf),
            "end": datetime.strptime("00:00", hf) + timedelta(days=1),
        },
    }

    # The payment for each interval in each day type
    payments = {WD: {"n": 25, "d": 15, "e": 20}, WE: {"n": 30, "d": 20, "e": 25}}

    # The precedence of the intervals
    interval_precedence = OrderedDict({"n": "d", "d": "e"})

    day_salary = 0

    day = day_data[:2]  # The day abbreviation
    day_type = days[day]  # The type of the day
    # Split the start and end of the day hours interval
    hours_interval = day_data[2:].split("-")
    start = datetime.strptime(hours_interval[0], hf)
    end = datetime.strptime(hours_interval[1], hf)
    # If the ending hour is the 00:00, add one day to signal that it is the end of the day
    # not the beginning
    if end == datetime.strptime("00:00", hf):
        end += timedelta(days=1)

    initial_interval = None
    end_interval = None
    # Found the intervals where the day working hours start and end
    for day_turn, turn_interval_hours in day_intervals.items():
        if turn_interval_hours["begin"] <= start <= turn_interval_hours["end"]:
            initial_interval = day_turn
        if turn_interval_hours["begin"] <= end <= turn_interval_hours["end"]:
            end_interval = day_turn

    current_start = start
    current_interval = initial_interval
    pay_data = []
    # If the current interval and the end interval are the same, calculate the amount
    # of hours worked and break the loop.
    # If not, calculate the amount of hours from the current start to the end of the
    # interval and update current interval and current start with the following interval
    # and current end with the end of the current interval.
    while True:
        if current_interval == end_interval:
            hours = round((end - current_start) / timedelta(hours=1), 2)
            pay_data.append(
                {"day_type": day_type, "interval": current_interval, "hours": hours}
            )
            break
        else:
            current_end = day_intervals[current_interval]["end"]
            hours = round((current_end - current_start) / timedelta(hours=1), 2)
            pay_data.append(
                {"day_type": day_type, "interval": current_interval, "hours": hours}
            )
            current_interval = interval_precedence[current_interval]
            current_start = day_intervals[current_interval]["begin"]

    # Calculate the pay for the day and add it to result
    for item in pay_data:
        day_salary += payments[item["day_type"]][item["interval"]] * item["hours"]

    return day_salary
