# -*- coding: utf-8 -*-
"""
Module for holding a platform account statement.

Copyright 2018-04-29 ChrisRBe
"""
import logging
from datetime import datetime


class Statement():
    """
    Implementation of the statement
    """
    def __init__(self, config, statement):
        """
        Constructor for Statement
        """
        self._config = config
        self._statement = statement

    def get_category(self):
        """
        Check the category of the given statement.

        :return: category of the statement; if unkown return the empty string
        """
        booking_type = self._statement[self._config.get_booking_type()]
        category = ""
        if self._config.get_relevant_income_regex().match(booking_type):
            category = 'Zinsen'
        elif self._config.get_relevant_invest_regex().match(booking_type):
            category = 'Einlage'
        elif self._config.get_relevant_payment_regex().match(booking_type):
            category = 'Entnahme'
        elif self.is_fee(booking_type):
            category = 'Gebühren'
        else:
            logging.debug(self._statement)
        return category

    def is_fee(self, booking_type):
        """ check if it is a statement with a fee"""
        return self._config.get_relevant_fee_regex() and self._config.get_relevant_fee_regex().match(booking_type)

    def get_date(self):
        """ get the date of the statement """
        return datetime.strptime(self._statement[self._config.get_booking_date()], self._config.get_booking_date_format()).date()

    def get_value(self):
        """ get the value of the statement """
        return self._statement[self._config.get_booking_value()].replace('.', ',')

    def get_note(self):
        """ get the note of the statement """
        return "{id}: {details}".format(id=self._statement[self._config.get_booking_id()],
                                        details=self._statement[self._config.get_booking_details()])

    def get_currency(self):
        """
        Check the currency of the given statement.

        :return: currency of the statement; if unkown return 'EUR'
        """
        if self._config.get_booking_currency():
            return self._statement[self._config.get_booking_currency()]
        else:
            return 'EUR'
