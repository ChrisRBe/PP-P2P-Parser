# -*- coding: utf-8 -*-
"""
Module for holding a platform account statement.

Copyright 2018-10-16 ChrisRBe
"""
import logging
from datetime import datetime


class Statement:
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

        :return: category of the statement; if unknown return the empty string
        """
        booking_type = self._statement[self._config.get_booking_type()]
        category = ""

        regex_to_category_mappings = [
            {
                "regex": self._config.get_relevant_income_regex(),
                "category": "Zinsen"
            },
            {
                "regex": self._config.get_relevant_invest_regex(),
                "category": "Einlage"
            },
            {
                "regex": self._config.get_relevant_payment_regex(),
                "category": "Entnahme"
            },
            {
                "regex": self._config.get_relevant_fee_regex(),
                "category": "Gebühren"
            },
            {
                "regex": self._config.get_special_entry_regex(),
                "category": "Undecided"
            },
            {
                "regex": self._config.get_ignorable_entry_regex(),
                "category": "Ignored"
            }
        ]

        for mapping in regex_to_category_mappings:
            if mapping["regex"] and mapping["regex"].match(booking_type):
                category = mapping["category"]
                break

        # This is currently a special case for the mintos "discount/premium" secondary market transactions parsing,
        # where an entry might be a fee or an income depending on its sign.
        if category == "Undecided":
            if self.get_value() >= 0:
                category = "Zinsen"
            elif self.get_value() < 0:
                category = "Gebühren"
            else:
                category = "Ignored"
                logging.debug("Unexpected value: ", self._statement)

        if category == "":
            logging.debug("Unexpected statement: ", self._statement)

        return category

    def is_fee(self, booking_type):
        """ check if it is a statement with a fee"""
        return self._config.get_relevant_fee_regex() and self._config.get_relevant_fee_regex().match(booking_type)

    def get_date(self):
        """ get the date of the statement """
        if self._statement[self._config.get_booking_date()]:
            statement_date = datetime.strptime(
                self._statement[self._config.get_booking_date()], self._config.get_booking_date_format()
            ).date()
        else:
            statement_date = datetime(1970, 1, 1).date()
        return statement_date

    def get_value(self):
        """ get the value of the statement """
        return float(self._statement[self._config.get_booking_value()].replace(",", "."))

    def get_note(self):
        """ get the note of the statement """
        return "{id}: {details}".format(
            id=self._statement[self._config.get_booking_id()],
            details=self._statement[self._config.get_booking_details()],
        )

    def get_currency(self):
        """
        Check the currency of the given statement.

        :return: currency of the statement; if unknown return 'EUR'
        """
        if self._config.get_booking_currency():
            return self._statement[self._config.get_booking_currency()]
        else:
            return "EUR"
