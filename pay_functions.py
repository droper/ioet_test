"""
Payment functions
"""

from datetime import datetime, time, timedelta

import re

from collections import OrderedDict


def read_week_data(data_file_handler):
    """
    Read each line in the data file, clean and validate. If valid add to the return list,
    if not include an error message.

    :param data_file_handler: file handler
    :return: list of dicts with two keys, valid and text
    """
    data_string_pattern = (
        r"^[A-Z]+=(?:(?:MO|TU|WE|TH|FR|SA|SU)\d{2}:\d{2}-\d{2}:\d{2},?)+$"
    )

    data_strings = []
    for count, data_string in enumerate(data_file_handler.readlines(), 1):
        data_string = data_string.strip()
        if re.match(data_string_pattern, data_string):
            data_strings.append({"valid": True, "text": data_string})
        else:
            data_strings.append(
                {
                    "valid": False,
                    "text": f"Data string number {count} does not comply with the format: {data_string}",
                }
            )

    return data_strings


def worker_pay(data):
    """
    Receives a string with the worker name and week hours worked.

    :param data: Data string with the format 'NAME=WD##:##-##:##,WD##:##-##:##' where WD is the
                 abbreviation of the day.
    :return: The amount of dollars to pay for each worker.
    """

    parts = data.split("=")
    name = parts[0]
    week_hours = parts[1]

    return f"The amount to pay {name} is: {week_pay(week_hours)} USD"


def week_pay(week_data):
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


def day_pay(day_data):
    """
    Receives a working day data and returns the payment for that day

    :param day_data: string in the format WD##:##
    :return: a float with the amount of dollars for the day
    """
    days = {
        "MO": "wd",
        "TU": "wd",
        "WE": "wd",
        "TH": "wd",
        "FR": "wd",
        "SA": "we",
        "SU": "we",
    }

    hf = "%H:%M"

    day_intervals = {
        "n": [datetime.strptime("00:00", hf), datetime.strptime("9:00", hf)],
        "d": [datetime.strptime("9:00", hf), datetime.strptime("18:00", hf)],
        "e": [
            datetime.strptime("18:00", hf),
            datetime.strptime("00:00", hf) + timedelta(days=1),
        ],
    }

    payments = {"wd": {"n": 25, "d": 15, "e": 20}, "we": {"n": 30, "d": 20, "e": 25}}

    interval_precedence = OrderedDict({"n": "d", "d": "e"})

    result = 0

    day = day_data[:2]  # The day abbreviation
    day_type = days[day]  # The type of the day
    # Split the start and end of the day hours interval
    hours_interval = day_data[2:].split("-")
    start = datetime.strptime(hours_interval[0], hf)
    end = datetime.strptime(hours_interval[1], hf)
    if end == datetime.strptime("00:00", hf):
        end += timedelta(days=1)

    initial_interval = None
    end_interval = None
    # Found the intervals where the day working hours start and end
    for k, v in day_intervals.items():
        if v[0] <= start <= v[1]:
            initial_interval = k
        if v[0] <= end <= v[1]:
            end_interval = k

    current_start = start
    current_interval = initial_interval
    pay_data = []
    # If the current interval and the end interval are the same, calculate the amount
    # of hours worked and break the loop.
    # If not, calculate the amount of hours from the current start to the end of the
    # interval and update current interval with the following interval.
    while True:
        if current_interval == end_interval:
            hours = round((end - current_start) / timedelta(hours=1), 2)
            pay_data.append(
                {"day_type": day_type, "interval": current_interval, "hours": hours}
            )
            break
        else:
            current_end = day_intervals[current_interval][1]
            hours = round((current_end - current_start) / timedelta(hours=1), 2)
            pay_data.append(
                {"day_type": day_type, "interval": current_interval, "hours": hours}
            )
            current_interval = interval_precedence[current_interval]
            current_start = day_intervals[current_interval][0]

    # Calculate the pay for the day and add it to result
    for item in pay_data:
        result += payments[item["day_type"]][item["interval"]] * item["hours"]

    return result
