<h1 align="center">PP-P2P-Parser</h1>

<p align="center">
<a href="https://github.com/ChrisRBe/PP-P2P-Parser/actions"><img alt="Action Status" src="https://github.com/ChrisRBe/PP-P2P-Parser/workflows/Integration/badge.svg?branch=master"></a>
<a href="https://codeclimate.com/github/ChrisRBe/PP-P2P-Parser/test_coverage"><img alt="Test Coverage" src="https://api.codeclimate.com/v1/badges/f3bad303efd4200ebee2/test_coverage"/></a>
<a href="https://codeclimate.com/github/ChrisRBe/PP-P2P-Parser/maintainability"><img alt="Maintainability" src="https://api.codeclimate.com/v1/badges/f3bad303efd4200ebee2/maintainability"/></a>
<a href="https://github.com/pre-commit/pre-commit"><img alt="pre-commit: enabled" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" style="max-width:100%;"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://app.bors.tech/repositories/37041"><img alt="Bors enabled" src="https://bors.tech/images/badge_small.svg"></a>
</p>

## Introduction

Application to read account statement files from different peer to peer lending sites,
e.g. mintos.com, and produces a Portfolio Performance readable csv file.

Input format needs to be a csv file as well!

## Usage

```text
parse-account-statements.py --help
usage:
An application to read account statement files from different peer to peer lending sites, e.g. Mintos.com and creates
a Portfolio Performance readable csv file.

NOTE: The output only contains interest and interest like payments received. No other statements are currently parsed.

List of currently supported providers:
    - Bondora
    - Bondora Grow Go
    - Estateguru
    - Lande
    - Mintos
    - Robocash
    - Swaper
    - Debitum Network
    - Viainvest

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

### Example

```shell
./parse-account-statements.py --type mintos src/test/testdata/mintos.csv
```

## &#x26a0; Information

&#x26a0; If you are using the --aggregate=monthly option, please note that this aggregates account activities
always on then last day of the month. This can lead to import issues in Portfolio Performance when importing
data for the current month.

E.g. import date is the 15th of a July, the account statement contains data with a date of 31st of July.

Account activity for a "future date" will be ignored/ not imported by Portfolio Performance.

Please note, that this behaviour on application side is intentional to avoid importing account activity
multiple times in Portfolio Performance.

## Currently supported formats

* `mintos` - Supports current account-statement.csv file format
* `estateguru` - Supports current German layout account statement csv file format
* `estateguru_en` - Adaptation for the English account statement csv file format
* `robocash` - Supports current account statement format (as of 2018-05-01) exported to csv
* `swaper` - Supports current account statement format (as of 2018-05-01) exported to csv
* `bondora` - Supports current account statement format (as of 2019-10-12); exported to csv
* `bondora_go_grow` - Supports current account statement format (as of 2019-10-12); exported to csv
* `debitumnetwork` - Supports current account statement format (as of 2020-09-08) exported to csv
* `viainvest` - Supports current account statement (as of 2021-12-12) exported as csv (Withdrawals do not work yet)
* `lande` - Supports current account statement (as of 2022-12-01) exported as csv (Withdrawals not tested yet)

### Alternative solution for Auxmoney

Unfortunately, the output file of Auxmoney's reports is not suitable for being parsed by PP-P2P-Parser in a meaningful way.
As an alternative, you can check out the [PP-Auxmoney-Parser](https://github.com/StegSchreck/PP-Auxmoney-Parser) project.

## Configuration files

Configuration for this script is stored in yaml files located under the config subdirectory.
The content directly reflects the format of the source account statement files.

Example:

```yaml
---
type_regex: !!map
  deposit: "(Deposits)|(^Incoming client.*)|(^Incoming currency exchange.*)|(^Affiliate partner bonus$)"
  withdraw: "(^Withdraw application.*)|(Outgoing currency.*)|(Withdrawal)"
  interest: "(^Delayed interest.*)|(^Late payment.*)|(^Interest income.*)|(^Cashback.*)|(^.*[Ii]nterest received.*)|(^.*late fees received$)"
  fee: "(^FX commission.*)|(.*secondary market fee$)"
  ignorable_entry: ".*investment in loan.*|.*[Pp]rincipal received.*|.*secondary market transaction.*"
  special_entry: "(.*discount/premium.*)"

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

* Python 3.8+ (unit tests are run against Python 3.8, 3.9, 3.10, 3.11)
* virtualenv
* pipenv

Installation of Python dependencies can be handled in two ways:

*   Install dependencies via `pip install -r requirements.txt`
*   Create a virtual environment using pipenv (**preferred way**)

    ```shell
    pipenv install
    pipenv shell
    ```

## Development

To set up a local development environment for this project please use either
of these two options:

*   Using plain pip

    ```shell
    pip install -r dev-requirements.txt
    ```

*   Using pipenv

    ```shell
    pipenv install --dev
    pipenv shell
    ```

## Legal

I'm not a lawyer. This project is in no way affiliated with
[Portfolio Performance](http://www.portfolio-performance.info/portfolio/),
but intended to be used with it.
