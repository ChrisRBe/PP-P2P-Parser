# PP-P2P-Parser

## Status

[![Build Status](https://travis-ci.org/ChrisRBe/PP-P2P-Parser.svg?branch=master)](https://travis-ci.org/ChrisRBe/PP-P2P-Parser)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/23ae124125c9439b8bd8087cf8efda20)](https://app.codacy.com/app/chrisrbe/PP-P2P-Parser?utm_source=github.com&utm_medium=referral&utm_content=ChrisRBe/PP-P2P-Parser&utm_campaign=badger)
[![Maintainability](https://api.codeclimate.com/v1/badges/f3bad303efd4200ebee2/maintainability)](https://codeclimate.com/github/ChrisRBe/PP-P2P-Parser/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f3bad303efd4200ebee2/test_coverage)](https://codeclimate.com/github/ChrisRBe/PP-P2P-Parser/test_coverage)

## Overview

Application to read account statement files from different peer to peer lending sites,
e.g. Mintos.com and produce a Portfolio Performance readable csv file

Currently supported provider: Mintos, Estateguru

## Requirements

Python 3 (implemented with python 3.6.4)


## Usage

parse-account-statements.py --help
usage: parse-account-statements.py [-h] [--type TYPE] [--debug] infile

positional arguments:
  infile       CSV file containing the downloaded data from the P2P site

optional arguments:
  -h, --help   show this help message and exit
  --type TYPE  Specifies the p2p lending operator
  --debug      enables debug level logging if set

## Currently supported types

mintos - Supports current account-statement.csv file format
estateguru - Supports current German layout account statement csv file format

## Output

CSV file format compatible with Performance Portfolio (German language setting)

## Legal

I'm not a lawyer. This project is in no way affiliated with
[Portfolio Performance](http://www.portfolio-performance.info/portfolio/),
but intended to be used with it.
