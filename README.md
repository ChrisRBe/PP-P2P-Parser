# PP-P2P-Parser

## Code Status

![](https://github.com/ChrisRBe/PP-P2P-Parser/workflows/Integration/badge.svg?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Maintainability](https://api.codeclimate.com/v1/badges/f3bad303efd4200ebee2/maintainability)](https://codeclimate.com/github/ChrisRBe/PP-P2P-Parser/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f3bad303efd4200ebee2/test_coverage)](https://codeclimate.com/github/ChrisRBe/PP-P2P-Parser/test_coverage)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Bors enabled](https://bors.tech/images/badge_small.svg)](https://app.bors.tech/repositories/37041)

## Introduction

Application to read account statement files from different peer to peer lending sites,
e.g. mintos.com, and produces a Portfolio Performance readable csv file.

Input format needs to be a csv file as well!

## Usage

```
parse-account-statements.py --help
usage:
An application to read account statement files from different peer to peer lending sites, e.g. Mintos.com and creates
a Portfolio Performance readable csv file.

NOTE: The output only contains interest and interest like payments received. No other statements are currently parsed.

List of currently supported providers:
    - Bondora
    - Bondora Grow Go
    - Estateguru
    - Mintos
    - Robocash
    - Swaper
    - Debitum Network

Control the way how account statements are processed via the aggregate parameter:
    - transaction: Currently does not process the input data beyond making it Portfolio Performance compatible.
    - daily: This aggregates all bookings of the same type into one statement per type and day.
    - monthly: This aggregates all bookings of the same type into one statement per type and month. Sets
            the last day of the month as transaction date.

Default behaviour for now is 'transaction'.

Copyright 2018-03-17 ChrisRBe

positional arguments:
  infile                CSV file containing the downloaded data from the P2P site

optional arguments:
  -h, --help            show this help message and exit
  --aggregate {transaction,daily,monthly}
                        specify how account statements should be summarized
  --type TYPE           Specifies the p2p lending operator
  --debug               enables debug level logging if set
```

```
parse-account-statements.py  --type mintos src/test/testdata/mintos.csv
```

> &#x26a0; If you are using the --aggregate=monthly option, please note that this application aggregates always on the
> last day of the month. This can lead to import issues in Portfolio Performance when importing data for
> the current month.
>
> E.g. import date is the 15th of a July, the account statement contains data with a date of 31st of July.
>
> Account activity for a "future date" will be ignored/ not imported by Portfolio Performance.
>
> Please note, that this behaviour on this application side is intentional to avoid importing account activity multiple
> times in Portfolio Performance.

## Currently supported formats

* mintos - Supports current account-statement.csv file format
* estateguru - Supports current German layout account statement csv file format
* robocash - Supports current account statement format (as of 2018-05-01) exported to csv
* swaper - Supports current account statement format (as of 2018-05-01) exported to csv
* bondora - Supports current account statement format (as of 2019-10-12); exported to csv
* bondora go & grow - Supports current account statement format (as of 2019-10-12); exported to csv
* debitumnetwork - Supports current account statement format (as of 2020-09-08) exported to csv

### Alternative solution for Auxmoney

Unfortunately, the output file of Auxmoney's reports is not suitable for being parsed by PP-P2P-Parser in a meaningful way.
As an alternative, you can check out the [PP-Auxmoney-Parser](https://github.com/StegSchreck/PP-Auxmoney-Parser) project.

## Configuration files

Configuration for this script is stored in yaml files located under the config subdirectory.
The content directly reflects the format of the source account statement files.

Example:

```
---
type_regex: !!map
  deposit: "^Incoming client.*"
  withdraw: "^Withdraw application.*"
  interest: "(^Delayed interest.*)|(^Late payment.*)|(^Interest income.*)|(^Cashback.*)"

csv_fieldnames:
  booking_date: 'Date'
  booking_date_format: '%Y-%m-%d %H:%M:%S'
  booking_details: 'Details'
  booking_id: 'Transaction ID'
  booking_type: 'Details'
  booking_value: 'Turnover'

```

## Output

CSV file format compatible with Performance Portfolio (German language setting).

## Dependencies

To use this application the following dependencies need to be installed:

* Python 3.6+ (unit test are run against Python 3.6, 3.7, 3.8, 3.9)
* PyYaml

Installation of Python dependencies can be handled in two ways:

*   Install dependencies via `pip install -r requirements.txt`
*   Create a virtual environment using pipenv

        pipenv install
        pipenv shell

## Legal

I'm not a lawyer. This project is in no way affiliated with
[Portfolio Performance](http://www.portfolio-performance.info/portfolio/),
but intended to be used with it.
