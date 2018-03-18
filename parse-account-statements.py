#!/usr/bin/python3
# Copyright 2018-03-17 ChrisRBe
import argparse
import csv
import logging
import os
import re
from datetime import datetime

relevant_invest_strings = "Incoming client"
relevant_income_strings = "^Delayed interest.*|^Late payment.*|^Interest income.*|^Cashback.*"


def main(infile, p2p_operator_name='mintos'):
    if os.path.exists(infile):
        input_file = infile
    else:
        return

    out_csv_fieldnames = ['Datum', 'Wert', 'Typ', 'Notiz']

    with open(input_file, newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        statement = csv.DictReader(csvfile, dialect=dialect)

        logging.debug(statement.fieldnames)

        relevant_income_regex = re.compile(relevant_income_strings)
        relevant_invest_regex = re.compile(relevant_invest_strings)

        with open(os.path.join(os.path.dirname(input_file), "portfolio_performance__{}.csv".format(p2p_operator_name)),
                  'w') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=out_csv_fieldnames, dialect=dialect)
            writer.writeheader()
            for entry in statement:
                category = ""
                if relevant_income_regex.match(entry['Details']):
                    category = "Zinsen"
                elif relevant_invest_regex.match(entry['Details']):
                    category = "Einlage"

                date = datetime.strptime(entry['Date'], "%Y-%m-%d %H:%M:%S")
                note = "{id}: {details}".format(id=entry['Transaction ID'], details=entry['Details'])

                formatted_account_entry = {out_csv_fieldnames[0]: date.date(),
                                           out_csv_fieldnames[1]: entry['Turnover'],
                                           out_csv_fieldnames[2]: category,
                                           out_csv_fieldnames[3]: note}
                logging.debug(formatted_account_entry)
                if category:
                    writer.writerow(formatted_account_entry)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=str,
                        help='CSV file containing the downloaded data from the P2P site')
    parser.add_argument('--type',
                        type=str,
                        help='Specifies the format of the input file (different for each P2P service)')
    parser.add_argument('--debug',
                        action='store_true',
                        help='enables debug level logging if set')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    main(args.infile, args.type)
