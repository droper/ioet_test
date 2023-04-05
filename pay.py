"""
Read the payment data and prints the week pay amount for each worker.
"""

import argparse

from paylib import worker_pay, read_week_data


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

    parser = argparse.ArgumentParser(
        description="Calculate the week payments for the workers in the file"
    )
    parser.add_argument(
        "-f", "--file", type=str, help="file path to read", default="pay_data.txt"
    )
    args = parser.parse_args()
    file_path = args.file

    with open(file_path, "r+") as f:
        for pay_string in pay(f):
            print(pay_string)
