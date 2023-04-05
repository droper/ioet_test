"""
Read the payment data and prints the week pay amount for each worker.
"""

from lib import worker_pay, read_week_data


def pay(data_file_handler):
    """
    Receives the handler of the data file and returns a list of strings with each
    worker payment for valid strings and an error message for invalid ones.
    :param data_file_handler: file handler
    :return: list of strings
    """

    result_strings = []
    workers_week_data = read_week_data(data_file_handler)

    for worker_week_data in workers_week_data:
        if worker_week_data["valid"]:
            result_strings.append(worker_pay(worker_week_data["text"]))
        else:
            result_strings.append(worker_week_data["text"])
    return result_strings


if __name__ == "__main__":
    with open("pay_data.txt", "r+") as f:
        for pay_string in pay(f):
            print(pay_string)
