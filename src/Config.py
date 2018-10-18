# -*- coding: utf-8 -*-
"""
Module for holding the coniguration of a platform.

Copyright 2018-04-29 ChrisRBe
"""
import logging
import re


class Config():
    """
    Implementation of the configuration
    """
    def __init__(self, config):
        """
        Constructor for Config
        """
        logging.info("Config ini")
        self._relevant_invest_regex = re.compile(config['type_regex']['deposit'])
        self._relevant_payment_regex = re.compile(config['type_regex']['withdraw'])
        self._relevant_income_regex = re.compile(config['type_regex']['interest'])
        if 'fee' in config['type_regex']:
            self._relevant_fee_regex = re.compile(config['type_regex']['fee'])
        else:
            self._relevant_fee_regex = None

        self._booking_date = config['csv_fieldnames']['booking_date']
        self._booking_date_format = config['csv_fieldnames']['booking_date_format']
        self._booking_details = config['csv_fieldnames']['booking_details']
        self._booking_id = config['csv_fieldnames']['booking_id']
        self._booking_type = config['csv_fieldnames']['booking_type']
        self._booking_value = config['csv_fieldnames']['booking_value']
        if 'booking_currency' in config['csv_fieldnames']:
            self._booking_currency = config['csv_fieldnames']['booking_currency']
        else:
            self._booking_currency = ''

    def get_relevant_invest_regex(self):
        """ get the relevant_invest_regex """
        return self._relevant_invest_regex

    def get_relevant_payment_regex(self):
        """ get the relevant_payment_regex """
        return self._relevant_payment_regex

    def get_relevant_income_regex(self):
        """ get the relevant_income_regex """
        return self._relevant_income_regex

    def get_relevant_fee_regex(self):
        """ get the relevant_fee_regex """
        return self._relevant_fee_regex

    def get_booking_date(self):
        """ get the booking_date """
        return self._booking_date

    def get_booking_date_format(self):
        """ get the booking_date_format """
        return self._booking_date_format

    def get_booking_details(self):
        """ get the booking_details """
        return self._booking_details

    def get_booking_id(self):
        """ get the booking_id """
        return self._booking_id

    def get_booking_type(self):
        """ get the booking_type """
        return self._booking_type

    def get_booking_value(self):
        """ get the booking_value """
        return self._booking_value

    def get_booking_currency(self):
        """ get the booking_currency """
        return self._booking_currency
