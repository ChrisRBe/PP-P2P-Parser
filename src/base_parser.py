# -*- coding: utf-8 -*-
"""
Module for a base peer to peer loan account statement parser

Copyright 2018-04-29 ChrisRBe
"""
import codecs
import csv
import logging
import os

from datetime import datetime
from .portfolio_performance_writer import PP_FIELDNAMES


class BaseParser(object):
    """
    Implementation of a base p2p account statement parser
    """
    def __init__(self):
        """
        Constructor for BaseParser
        """
        self._account_statement_file = None
        self.output_list = []

        self.booking_date = ''
        self.booking_date_format = ''
        self.booking_details = ''
        self.booking_id = ''
        self.booking_type = ''
        self.booking_value = ''

        self.relevant_invest_regex = None
        self.relevant_payment_regex = None
        self.relevant_income_regex = None

    @property
    def account_statement_file(self):
        """account statement file property"""
        return self._account_statement_file

    @account_statement_file.setter
    def account_statement_file(self, value):
        """account statement file property setter"""
        self._account_statement_file = value

    def parse_account_statement(self):
        """
        read a Estateguru account statement csv file and filter the content according to the defined strings

        :return:
        """
        if os.path.exists(self._account_statement_file):
            with codecs.open(self._account_statement_file, 'r', encoding='utf-8') as infile:
                dialect = csv.Sniffer().sniff(infile.readline())
                infile.seek(0)
                account_statement = csv.DictReader(infile, dialect=dialect)
                for statement in account_statement:
                    if self.relevant_income_regex.match(statement[self.booking_type]):
                        category = "Zinsen"
                    elif self.relevant_invest_regex.match(statement[self.booking_type]):
                        category = 'Einlage'
                    elif self.relevant_payment_regex.match(statement[self.booking_type]):
                        category = 'Entnahme'
                    else:
                        logging.debug(statement)
                        continue

                    booking_date = datetime.strptime(statement[self.booking_date], self.booking_date_format)
                    note = "{id}: {details}".format(id=statement[self.booking_id],
                                                    details=statement[self.booking_details])

                    formatted_account_entry = {PP_FIELDNAMES[0]: booking_date.date(),
                                               PP_FIELDNAMES[1]: statement[self.booking_value].replace('.', ','),
                                               PP_FIELDNAMES[2]: category,
                                               PP_FIELDNAMES[3]: note}
                    self.output_list.append(formatted_account_entry)
        else:
            logging.error("Account statement file {} does not exist.".format(self.account_statement_file))
        return self.output_list
