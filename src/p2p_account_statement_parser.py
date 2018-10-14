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
        self.config = None

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
        Parse the YAML configuration file containing specific settings for the individual p2p loan platform

        :return:
        """
        with open(self.config_file, 'r', encoding='utf-8') as ymlconfig:
            yaml = YAML(typ='safe')
            config = yaml.load(ymlconfig)
            self.config = Config(config)

    def parse_account_statement(self):
        """
        read a platform account statement csv file and filter the content according to the defined strings

        :return:
        """
        if os.path.exists(self._account_statement_file):
            self.__parse_service_config()
            with codecs.open(self._account_statement_file, 'r', encoding='utf-8-sig') as infile:
                dialect = csv.Sniffer().sniff(infile.readline())
                infile.seek(0)
                account_statement = csv.DictReader(infile, dialect=dialect)
                for statement in account_statement:
                    sttmnt = Statement(self.config, statement)
                    category = sttmnt.get_category()
                    if not category:
                        continue

                    formatted_account_entry = {PP_FIELDNAMES[0]: sttmnt.get_date(),
                                               PP_FIELDNAMES[1]: sttmnt.get_value(),
                                               PP_FIELDNAMES[2]: sttmnt.get_currency(),
                                               PP_FIELDNAMES[3]: category,
                                               PP_FIELDNAMES[4]: sttmnt.get_note()}
                    self.output_list.append(formatted_account_entry)
        else:
            logging.error("Account statement file {} does not exist.".format(self.account_statement_file))
        return self.output_list


class Config():
    """
    Implementation of the configuration
    """
    def __init__(self, config):
        """
        Constructor for Config
        """
        logging.info("Config ini")
        self.relevant_invest_regex = re.compile(config['type_regex']['deposit'])
        self.relevant_payment_regex = re.compile(config['type_regex']['withdraw'])
        self.relevant_income_regex = re.compile(config['type_regex']['interest'])
        if 'fee' in config['type_regex']:
            self.relevant_fee_regex = re.compile(config['type_regex']['fee'])
        else:
            self.relevant_fee_regex = None

        self.booking_date = config['csv_fieldnames']['booking_date']
        self.booking_date_format = config['csv_fieldnames']['booking_date_format']
        self.booking_details = config['csv_fieldnames']['booking_details']
        self.booking_id = config['csv_fieldnames']['booking_id']
        self.booking_type = config['csv_fieldnames']['booking_type']
        self.booking_value = config['csv_fieldnames']['booking_value']
        if 'booking_currency' in config['csv_fieldnames']:
            self.booking_currency = config['csv_fieldnames']['booking_currency']
        else:
            self.booking_currency = ''


class Statement():
    """
    Implementation of the statement
    """
    def __init__(self, config, statement):
        """
        Constructor for Statement
        """
        self.config = config
        self._statement = statement

    def get_category(self):
        """
        Check the category of the given statement.

        :return: category of the statement; if unkown return the empty string
        """
        booking_type = self._statement[self.config.booking_type]
        category = ""
        if self.config.relevant_income_regex.match(booking_type):
            category = 'Zinsen'
        elif self.config.relevant_invest_regex.match(booking_type):
            category = 'Einlage'
        elif self.config.relevant_payment_regex.match(booking_type):
            category = 'Entnahme'
        elif self.is_fee(booking_type):
            category = 'Gebühren'
        else:
            logging.debug(self._statement)
        return category

    def is_fee(self, booking_type):
        """ check if it is a statement with a fee"""
        return self.config.relevant_fee_regex and self.config.relevant_fee_regex.match(booking_type)

    def get_date(self):
        """ get the date of the statement """
        return datetime.strptime(self._statement[self.config.booking_date], self.config.booking_date_format).date()

    def get_value(self):
        """ get the value of the statement """
        return self._statement[self.config.booking_value].replace('.', ',')

    def get_note(self):
        """ get the note of the statement """
        return "{id}: {details}".format(id=self._statement[self.config.booking_id],
                                        details=self._statement[self.config.booking_details])

    def get_currency(self):
        """
        Check the currency of the given statement.

        :return: currency of the statement; if unkown return 'EUR'
        """
        if self.config.booking_currency:
            return self._statement[self.config.booking_currency]
        else:
            return 'EUR'
