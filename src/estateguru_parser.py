# -*- coding: utf-8 -*-
"""
Module for the Estateguru account statement parser

Copyright 2018-04-30 ChrisRBe
"""
import re

from .base_parser import BaseParser


class EstateguruParser(BaseParser):
    """
    Implementation for the Estateguru account statement parser
    """
    def __init__(self):
        """
        Constructor for EstateguruParser
        """
        super().__init__()
        self.relevant_invest_regex = re.compile("^Einzahlung.*")
        self.relevant_payment_regex = re.compile("^Auszahlung.*")
        self.relevant_income_regex = re.compile("^Empfehlungsbonus.*|^Zins.*|^Sondervergütung.*")

        self.booking_date = 'Zahlungsdatum'
        self.booking_date_format = '%d/%m/%Y %H:%M'
        self.booking_details = 'Projektname'
        self.booking_id = 'UniqueId'
        self.booking_type = 'Cashflow-Typ'
        self.booking_value = 'Betrag'
