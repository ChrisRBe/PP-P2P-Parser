# Copyright 2018-04-29 ChrisRBe
# -*- coding: utf-8 -*-
import csv
import logging
import os
import re

from datetime import datetime
from .portfolio_performance_writer import PP_FIELDNAMES


class MintosParser(object):
    def __init__(self):
        """
        Constructor for MintosParser
        """
        self._account_statement_file = None
        self.output_list = []
        self.relevant_invest_regex = re.compile("Incoming client")
        self.relevant_income_regex = re.compile("^Delayed interest.*|^Late payment.*|^Interest income.*|^Cashback.*")

    @property
    def account_statement_file(self):
        return self._account_statement_file

    @account_statement_file.setter
    def account_statement_file(self, value):
        self._account_statement_file = value

    def parse_account_statement(self):
        """
        read a Mintos account statement csv file and filter the content according to the defined strings

        :return:
        """
        if os.path.exists(self._account_statement_file):
            with open(self._account_statement_file, 'r', newline='') as infile:
                dialect = csv.Sniffer().sniff(infile.readline())
                infile.seek(0)
                account_statement = csv.DictReader(infile, dialect=dialect)
                for statement in account_statement:
                    category = ''
                    if self.relevant_income_regex.match(statement['Details']):
                        category = "Zinsen"
                    elif self.relevant_invest_regex.match(statement['Details']):
                        category = "Einlage"
                    else:
                        logging.debug(statement)
                        continue

                    date = datetime.strptime(statement['Date'], "%Y-%m-%d %H:%M:%S")
                    note = "{id}: {details}".format(id=statement['Transaction ID'], details=statement['Details'])

                    formatted_account_entry = {PP_FIELDNAMES[0]: date.date(),
                                               PP_FIELDNAMES[1]: statement['Turnover'],
                                               PP_FIELDNAMES[2]: category,
                                               PP_FIELDNAMES[3]: note}
                    if category:
                        self.output_list.append(formatted_account_entry)
            return self.output_list
