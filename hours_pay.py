"""
The company ACME offers their employees the flexibility to work the hours they want. They will pay for the
hours worked based on the day of the week and datetime of day, according to the following table:

Monday - Friday

00:01 - 09:00 25 USD
09:01 - 18:00 15 USD
18:01 - 00:00 20 USD

Saturday and Sunday

00:01 - 09:00 30 USD
09:01 - 18:00 20 USD
18:01 - 00:00 25 USD

The goal of this exercise is to calculate the total that the company has to pay an employee, based on
the hours they worked and the datetimes during which they worked. The following abbreviations will be
used for entering data:

MO: Monday
TU: Tuesday
WE: Wednesday
TH: Thursday
FR: Friday
SA: Saturday
SU: Sunday

Input: the name of an employee and the schedule they worked, indicating the datetime and hours. This should be
a .txt file with at least five sets of data. You can include the data from our two examples below.

Output: indicate how much the employee has to be paid

For example:

Case 1:

INPUT

RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00

OUTPUT:

The amount to pay RENE is: 215 USD

Case 2:

INPUT

ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00

OUTPUT:

The amount to pay ASTRID is: 85 USD
"""

from datetime import datetime, timedelta

from collections import OrderedDict


def pay(data):
    """
    Receives a week worked hours data and returns the amount of dollars to pay. For a day the amount of
    hours in each interval is calculated and used to multiply it for the hour salary.

    :param data: Data string with the format 'WD##:##-##:##,WD##:##-##:##' where WD is the abbreviation
                 of the day.
    :return: the amount of dollars to pay for each worker
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
        "n": [datetime.strptime("00:01", hf), datetime.strptime("9:00", hf)],
        "d": [datetime.strptime("9:01", hf), datetime.strptime("18:00", hf)],
        "e": [
            datetime.strptime("18:01", hf),
            datetime.strptime("00:00", hf) + timedelta(days=1),
        ],
    }

    payments = {"wd": {"n": 25, "d": 15, "e": 20}, "we": {"n": 30, "d": 20, "e": 25}}

    interval_precedence = OrderedDict({"n": "d", "d": "e"})

    # Split the data string into the day hours intervals
    week_hours = data.split(",")

    result = 0
    # Loop over each day in the data string, extract the day, day_type and hours in each day
    for day_hours in week_hours:
        day = day_hours[:2]  # The day abbreviation
        day_type = days[day]  # The type of the day
        hours_interval = day_hours[2:].split(
            "-"
        )  # Split the start and end of the day hours interval
        start = datetime.strptime(hours_interval[0], hf)
        end = datetime.strptime(hours_interval[1], hf)

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

    return round(result, 2)
