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

        :return: category of the statement; if ignored on purpose return 'Ignored', if unknown return the empty string
        """
        booking_type = self._statement[self._config.get_booking_type()]
        value = self.get_value()

        regex_to_category_mappings = [
            {"regex": self._config.get_relevant_income_regex(), "category": "Zinsen"},
            {"regex": self._config.get_relevant_invest_regex(), "category": "Einlage"},
            {"regex": self._config.get_relevant_payment_regex(), "category": "Entnahme"},
            {"regex": self._config.get_relevant_fee_regex(), "category": "Gebühren"},
            {"regex": self._config.get_special_entry_regex(), "category": "Undecided"},
            {"regex": self._config.get_ignorable_entry_regex(), "category": "Ignored"},
        ]

        category = ""
        for mapping in regex_to_category_mappings:
            category = self.__match_category(mapping, booking_type, value)
            if category:
                break

        if not category:
            logging.debug("Unexpected statement: ", self._statement)

        return category

    def get_date(self):
        """
        get the date of the statement

        :return: statement date as datetime object
        """
        if self._statement[self._config.get_booking_date()]:
            statement_date = datetime.strptime(
                self._statement[self._config.get_booking_date()], self._config.get_booking_date_format()
            ).date()
        else:
            statement_date = datetime(1970, 1, 1).date()
        return statement_date

    def get_value(self):
        """
        get the value of the statement

        :return: value of the current statement as float.
        """
        raw_value = self._statement[self._config.get_booking_value()]
        return Statement._parse_value(raw_value)

    def get_note(self):
        """
        get the note of the statement

        :return: any note added in the original csv.
        """
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
    
    @staticmethod
    def _parse_value(value):
        if not value:
            return None

        dot_pos = value.find(".")
        comma_pos = value.find(",")

        # Check position of . and , to replace them in the right order
        if dot_pos != -1 and comma_pos != -1:
            if dot_pos < comma_pos:
                value = value.replace(".", "")
            else:
                value = value.replace(",", "")
                
        return float(value.replace(",", "."))

    @staticmethod
    def __match_category(mapping, booking_type, value):
        """
        takes a dict of format {"regex": "compiled regex", "category": "category"} and returns the correct mapping for
        the category.

        :param mapping: dict of type {"regex": "compiled regex", "category": "category"}
        :param booking_type: string containing the relevant loan information to determine category of entry.
        :param value: value of the transaction, only required to handle special cases for mintos premium discount

        :return: category
        """
        category = ""
        if mapping["regex"] and mapping["regex"].match(booking_type):
            category = mapping["category"]
        if category == "Undecided":
            category = Statement.__handle_special_case_mintos_discount_premium(value)
        return category

    @staticmethod
    def __handle_special_case_mintos_discount_premium(value):
        """
        This is currently a special case for the Mintos "discount/premium" secondary market transactions parsing,
        where an entry might be a fee or an income depending on its sign.

        :param value: how much money was returned/paid

        :return: Zinsen if value >= 0 Gebühren in any other case
        """

        if value >= 0:
            return "Zinsen"
        else:
            return "Gebühren"
