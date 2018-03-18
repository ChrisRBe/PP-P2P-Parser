# PP-P2P-Parser
Parser for P2P service Mintos.com for Portfolio Performance.

# Requirements
Python 3 (implemented with python 3.6.4)

# Usage
parse-account-statements.py --help
usage: parse-account-statements.py [-h] [--type TYPE] [--debug] infile

positional arguments:
  infile       CSV file containing the downloaded data from the P2P site

optional arguments:
  -h, --help   show this help message and exit
  --type TYPE  Specifies the format of the input file (different for each P2P
               service)
  --debug      enables debug level logging if set

# Currently supported types
mintos - Supports current account-statement.csv file format

# Output
CSV file format compatible with Performance Portfolio (German language setting)

# Legal
I'm not a lawyer. This project is in no way affiliated with [Portfolio Performance](http://www.portfolio-performance.info/portfolio/), but intended to be used with it.
