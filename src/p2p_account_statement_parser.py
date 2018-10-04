# -*- coding: utf-8 -*-
"""
Module for a generic peer to peer loan account statement parser.

Copyright 2018-04-29 ChrisRBe
"""
import codecs
import csv
import logging
import os
import re

from datetime import datetime

from ruamel.yaml import YAML

from .portfolio_performance_writer import PP_FIELDNAMES


class PeerToPeerPlatformParser(object):
    """
    Implementation of a generic p2p investment platform account statement parser.
    Actual configuration for the individual services is done via a yml config file.
    """
    def __init__(self):
        """
        Constructor for PeerToPeerPlatformParser
        """
        self._account_statement_file = None
        self._config_file = None
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
        self.relevant_fee_regex = None

    @property
    def account_statement_file(self):
        """account statement file property"""
        return self._account_statement_file

    @account_statement_file.setter
    def account_statement_file(self, value):
        """account statement file property setter"""
        self._account_statement_file = value

    @property
    def config_file(self):
        """config file property"""
        return self._config_file

    @config_file.setter
    def config_file(self, value):
        """config file property setter"""
        self._config_file = value

    def __parse_service_config(self):
        """
        Parse the YAML configuration file containing specific settings for the individual peer to peer loan provider

        :return:
        """
        with open(self.config_file, 'r', encoding='utf-8') as ymlconfig:
            yaml = YAML(typ='safe')
            config = yaml.load(ymlconfig)

            self.relevant_invest_regex = re.compile(config['type_regex']['deposit'])
            self.relevant_payment_regex = re.compile(config['type_regex']['withdraw'])
            self.relevant_income_regex = re.compile(config['type_regex']['interest'])
            self.relevant_fee_regex = re.compile(config['type_regex']['fee'])

            self.booking_date = config['csv_fieldnames']['booking_date']
            self.booking_date_format = config['csv_fieldnames']['booking_date_format']
            self.booking_details = config['csv_fieldnames']['booking_details']
            self.booking_id = config['csv_fieldnames']['booking_id']
            self.booking_type = config['csv_fieldnames']['booking_type']
            self.booking_value = config['csv_fieldnames']['booking_value']
            self.booking_currency = config['csv_fieldnames']['booking_currency']

    def parse_account_statement(self):
        """
        read a Estateguru account statement csv file and filter the content according to the defined strings

        :return:
        """
        if os.path.exists(self._account_statement_file):
            self.__parse_service_config()
            with codecs.open(self._account_statement_file, 'r', encoding='utf-8-sig') as infile:
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
                    elif self.relevant_fee_regex.match(statement[self.booking_type]):
                        category = 'Gebühren'
                    else:
                        logging.debug(statement)
                        continue

                    booking_date = datetime.strptime(statement[self.booking_date], self.booking_date_format)
                    note = "{id}: {details}".format(id=statement[self.booking_id],
                                                    details=statement[self.booking_details])

                    formatted_account_entry = {PP_FIELDNAMES[0]: booking_date.date(),
                                               PP_FIELDNAMES[1]: statement[self.booking_value].replace('.', ','),
                                               PP_FIELDNAMES[2]: statement[self.booking_currency],
                                               PP_FIELDNAMES[3]: category,
                                               PP_FIELDNAMES[4]: note}
                    self.output_list.append(formatted_account_entry)
        else:
            logging.error("Account statement file {} does not exist.".format(self.account_statement_file))
        return self.output_list
