"""
Read the payment data and prints the week pay amount for each worker.
"""

import argparse

from paylib import pay


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
