# -*- coding: utf-8 -*-
"""
Module for the Estateguru account statement parser

Copyright 2018-04-30 ChrisRBe
"""
import codecs
import csv
import logging
import os
import re

from datetime import datetime
from .portfolio_performance_writer import PP_FIELDNAMES


class EstateguruParser(object):
    """
    Implementation for the Estateguru account statement parser
    """
    def __init__(self):
        """
        Constructor for MintosParser
        """
        self._account_statement_file = None
        self.output_list = []
        self.relevant_invest_regex = re.compile("^Einzahlung.*")
        self.relevant_payment_regex = re.compile("^Auszahlung.*")
        self.relevant_income_regex = re.compile("^Empfehlungsbonus.*|^Zins.*|^Sondervergütung.*")

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
                    category = ''
                    if self.relevant_income_regex.match(statement['Cashflow-Typ']):
                        category = "Zinsen"
                    elif self.relevant_invest_regex.match(statement['Cashflow-Typ']):
                        category = 'Einlage'
                    elif self.relevant_payment_regex.match(statement['Cashflow-Typ']):
                        category = 'Entnahme'
                    else:
                        logging.debug(statement)
                        continue

                    date = datetime.strptime(statement['Zahlungsdatum'], "%d/%m/%Y %H:%M")
                    note = "{id}: {details}".format(id=statement['UniqueId'], details=statement['Projektname'])

                    formatted_account_entry = {PP_FIELDNAMES[0]: date.date(),
                                               PP_FIELDNAMES[1]: statement['Betrag'],
                                               PP_FIELDNAMES[2]: category,
                                               PP_FIELDNAMES[3]: note}
                    if category:
                        self.output_list.append(formatted_account_entry)
            return self.output_list
