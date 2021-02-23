# -*- coding: utf-8 -*-
"""
Module for a generic peer to peer loan account statement parser.

Copyright 2018-04-29 ChrisRBe
"""
import calendar
import codecs
import csv
import logging

from yaml import safe_load

from src.Config import Config
from src.portfolio_performance_writer import PP_FIELDNAMES
from src.Statement import Statement


class PeerToPeerPlatformParser(object):
    """
    Implementation of a generic p2p investment platform account statement parser.
    Actual configuration for the individual services is done via a yml config file.
    """

    def __init__(self, config, infile):
        """
        Constructor for PeerToPeerPlatformParser
        """
        self._account_statement_file = infile
        self._config_file = config

        self.config = None
        self.output_list = []
        self.aggregation_data = {}

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

    def __aggregate_statements(self, formatted_account_entry, comment, monthly=True):
        entry_date = formatted_account_entry[PP_FIELDNAMES[0]]
        if monthly:
            last_day = calendar.monthrange(entry_date.year, entry_date.month)[1]
            entry_date = entry_date.replace(day=last_day)

        entry_type = formatted_account_entry[PP_FIELDNAMES[3]]
        logging.debug("entry type is {}. new entry date is {}".format(entry_type, entry_date))
        if entry_date not in self.aggregation_data:
            self.aggregation_data[entry_date] = {}
        if entry_type in self.aggregation_data[entry_date]:
            logging.debug("add to existing entry")
            self.aggregation_data[entry_date][entry_type][PP_FIELDNAMES[1]] += formatted_account_entry[
                PP_FIELDNAMES[1]
            ]
        else:
            self.aggregation_data[entry_date][entry_type] = {
                PP_FIELDNAMES[0]: entry_date,
                PP_FIELDNAMES[1]: formatted_account_entry[PP_FIELDNAMES[1]],
                PP_FIELDNAMES[2]: formatted_account_entry[PP_FIELDNAMES[2]],
                PP_FIELDNAMES[3]: entry_type,
                PP_FIELDNAMES[4]: comment,
            }

    def __aggregate_statements_daily(self, formatted_account_entry):
        self.__aggregate_statements(formatted_account_entry, "Tageszusammenfassung", False)

    def __aggregate_statements_monthly(self, formatted_account_entry):
        self.__aggregate_statements(formatted_account_entry, "Monatszusammenfassung", True)

    def __format_statement(self, statement):
        """
        Formats a given statement into a dictionary containing the relevant data for Portfolio Performance.

        :param statement: contains a line from the given CSV file

        :return: dictionary containing the formatted account entry
        """
        statement = Statement(self.config, statement)
        category = statement.get_category()

        if not category or category == "Ignored":
            return

        formatted_account_entry = {
            PP_FIELDNAMES[0]: statement.get_date(),
            PP_FIELDNAMES[1]: round(statement.get_value(), 9),
            PP_FIELDNAMES[2]: statement.get_currency(),
            PP_FIELDNAMES[3]: category,
            PP_FIELDNAMES[4]: statement.get_note(),
        }
        return formatted_account_entry

    def __migrate_data_to_output(self):
        """
        Iterates over the data collected for the aggregation of account statement data and adds it to the output list.
        :return:
        """
        for _, booking_type in self.aggregation_data.items():
            for _, entry in booking_type.items():
                entry[PP_FIELDNAMES[1]] = round(entry[PP_FIELDNAMES[1]], 9)
                self.output_list.append(entry)

    def __parse_service_config(self):
        """
        Parse the YAML configuration file containing specific settings for the individual p2p loan platform
        """
        with open(self.config_file, "r", encoding="utf-8") as ymlconfig:
            config = safe_load(ymlconfig)
            self.config = Config(config)

    def __process_statement(self, statement, aggregate="transaction"):
        """
        Processes each statement read from the account statement file. First, format in into the dictionary.
        Then check what aggregation should be applied.

            - transaction: add directly to the output list.
            - daily: add it to intermediate aggregation collection.
            - monthly: add it to intermediate aggregation collection.

        :param statement: Contains one line from the account statement file
        :param aggregate: specify the aggregation format; e.g. daily or monthly. Defaults to transaction.

        :return:
        """
        formatted_account_entry = self.__format_statement(statement)
        if formatted_account_entry:
            if aggregate == "transaction":
                self.output_list.append(formatted_account_entry)
            elif aggregate == "daily":
                self.__aggregate_statements_daily(formatted_account_entry)
            elif aggregate == "monthly":
                self.__aggregate_statements_monthly(formatted_account_entry)

    def parse_account_statement(self, aggregate="transaction"):
        """
        read a platform account statement csv file and filter the content according to the given configuration file.
        If aggregation is selected the output data will be post processed in the following way:

        - aggregate="transaction": return the list of processed statements as is.
        - aggregate="daily": return a list of post-processed statements aggregating on daily basis for each
          booking type.
        - aggregate="monthly": return a list of post-processed statements aggregating on monthly basis for each
          booking type.

        :param aggregate: specifies the aggregation period. defaults to daily.
        :return: list of account statement entries ready for use in Portfolio Performance
        """
        if aggregate == "transaction" or aggregate == "daily" or aggregate == "monthly":
            logging.info("Aggregating data on a {} basis".format(aggregate))
        else:
            logging.error("Aggregating data on a {} basis not supported.".format(aggregate))
            return

        self.__parse_service_config()

        with codecs.open(self._account_statement_file, "r", encoding="utf-8-sig") as infile:
            dialect = csv.Sniffer().sniff(infile.readline())
            infile.seek(0)
            account_statement = csv.DictReader(infile, dialect=dialect)

            for statement in account_statement:
                self.__process_statement(aggregate=aggregate, statement=statement)

        if aggregate == "daily" or aggregate == "monthly":
            self.__migrate_data_to_output()
        return self.output_list
