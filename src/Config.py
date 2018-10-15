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

    def get_relevant_invest_regex(self):
        """ get the relevant_invest_regex """
        return self.relevant_invest_regex

    def get_relevant_payment_regex(self):
        """ get the relevant_payment_regex """
        return self.relevant_payment_regex

    def get_relevant_income_regex(self):
        """ get the relevant_income_regex """
        return self.relevant_income_regex

    def get_relevant_fee_regex(self):
        """ get the relevant_fee_regex """
        return self.relevant_fee_regex

    def get_booking_date(self):
        """ get the booking_date """
        return self.booking_date

    def get_booking_date_format(self):
        """ get the booking_date_format """
        return self.booking_date_format

    def get_booking_details(self):
        """ get the booking_details """
        return self.booking_details

    def get_booking_id(self):
        """ get the booking_id """
        return self.booking_id

    def get_booking_type(self):
        """ get the booking_type """
        return self.booking_type

    def get_booking_value(self):
        """ get the booking_value """
        return self.booking_value

    def get_booking_currency(self):
        """ get the booking_currency """
        return self.booking_currency
