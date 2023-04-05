# Week payment calculator

## Introduction
The program read strings from a text file and use them to calculate the week payment for a worker. The string 
contains the worker name and each day turn beginning and ending.

Each day is divided in three turns:

* Night: 00:00 - 9:00
* Day: 9:00 - 18:00
* Evening: 18:00 - 00:00

There are different pay rates for week days and weekends:

| Turn    |Week day|weekend|
|---------|--------|----------|
| Night   | 25 | 30 |
| Day     | 15 | 20 |
| Evening | 20 | 25 |

The string format is like the following examples, with the worker name, the day abbreviations and
the hours of beginning and ending for each day work.

    FRED=MO00:03-11:00,TU11:00-11:30,TH08:00-20:00,SU18:00-23:00
    JHON=MO00:01-09:00,TH09:00-18:00,SU18:00-23:59

## Architecture

The software is divided in layers, each one is in charge of one task:

* Clean and validate the strings (this can be divided in more layers).
* Create the response for each worker data.
* Calculate the weekly payment for each worker
* Calculate a day payment 

There are tests for each function.

## Execution

To execute the program in a *nix machine:

* Open a terminal.
* Clone the repository: `git clone https://github.com/droper/ioet_test.git`
* Get into the repository directory: `cd ioet_test`
* Execute the program: `python pay.py`
* Run the tests: `python tests/test.py`

To add new strings to test the program, just open pay_data.txt and add new lines of text with a worker
week data.

