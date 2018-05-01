# -*- coding: utf-8 -*-
"""
Module for the Mintos account statement parser

Copyright 2018-04-29 ChrisRBe
"""
import re

from .base_parser import BaseParser


class MintosParser(BaseParser):
    """
    Implementation for the Mintos account statement parser
    """
    def __init__(self):
        """
        Constructor for MintosParser
        """
        super().__init__()
        self.relevant_invest_regex = re.compile("Incoming client")
        self.relevant_payment_regex = re.compile("^Withdraw application.*")
        self.relevant_income_regex = re.compile("^Delayed interest.*|^Late payment.*|^Interest income.*|^Cashback.*")

        self.booking_date = 'Date'
        self.booking_date_format = '%Y-%m-%d %H:%M:%S'
        self.booking_details = 'Details'
        self.booking_id = 'Transaction ID'
        self.booking_type = 'Details'
        self.booking_value = 'Turnover'
