# -*- coding: utf-8 -*-
"""
Module for a generic peer to peer loan account statement parser.

Copyright 2018-04-29 ChrisRBe
"""
import codecs
import csv
import logging
import os

from ruamel.yaml import YAML

from src.portfolio_performance_writer import PP_FIELDNAMES
from src.Config import Config
from src.Statement import Statement


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
