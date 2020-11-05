# PP-P2P-Parser

## Code Status

![](https://github.com/ChrisRBe/PP-P2P-Parser/workflows/Integration/badge.svg?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Maintainability](https://api.codeclimate.com/v1/badges/f3bad303efd4200ebee2/maintainability)](https://codeclimate.com/github/ChrisRBe/PP-P2P-Parser/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f3bad303efd4200ebee2/test_coverage)](https://codeclimate.com/github/ChrisRBe/PP-P2P-Parser/test_coverage)

## Overview

Application to read account statement files from different peer to peer lending sites,
e.g. Mintos.com and produce a Portfolio Performance readable csv file. Input format needs to be csv!

## Requirements

Python 3 (implemented with python 3.6.4)

## Dependencies

The configuration for this application is stored in yaml files. The module used for
loading yaml files is [ruamel.yaml](https://yaml.readthedocs.io/en/latest/).
Install via:

`pip install ruamel.yaml`

## Usage

```
parse-account-statements.py --help
usage: parse-account-statements.py [-h] [--type TYPE] [--debug] infile

positional arguments:
  infile       CSV file containing the downloaded data from the P2P site

optional arguments:
  -h, --help   show this help message and exit
  --type TYPE  Specifies the p2p lending operator
  --debug      enables debug level logging if set
```

```
parse-account-statements.py  --type mintos src/test/testdata/mintos.csv
```

## Currently supported formats

* mintos - Supports current account-statement.csv file format
* estateguru - Supports current German layout account statement csv file format
* robocash - Supports current account statement format (as of 2018-05-01) exported to csv
* swaper - Supports current account statement format (as of 2018-05-01) exported to csv
* bondora - Supports current account statement format (as of 2019-10-12); exported to csv
* bondora go & grow - Supports current account statement format (as of 2019-10-12); exported to csv
* debitumnetwork - Supports current account statement format (as of 2020-09-08) exported to csv

### Alternative solution for Auxmoney
Unfortunately, the output file of Auxmoney's reports is not suitable for being parsed by PP-P2P-Parser in a senseful way. As an alternative, you can check out the [PP-Auxmoney-Parser](https://github.com/StegSchreck/PP-Auxmoney-Parser) project.

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

CSV file format compatible with Performance Portfolio (German language setting)

## Legal

I'm not a lawyer. This project is in no way affiliated with
[Portfolio Performance](http://www.portfolio-performance.info/portfolio/),
but intended to be used with it.
