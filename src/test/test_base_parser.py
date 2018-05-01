# -*- coding: utf-8 -*-
"""
Unit test for the base parser module

Copyright 2018-05-01 ChrisRBe
"""
import datetime
import os
import re
from unittest import TestCase

from ..base_parser import BaseParser


class TestBaseParser(TestCase):
    """Test case implementation for BaseParser"""
    def setUp(self):
        """test case setUp, run for each test case"""
        self.base_parser = BaseParser()
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), 'testdata', 'mintos.csv')

        self.base_parser.relevant_invest_regex = re.compile("Incoming client")
        self.base_parser.relevant_payment_regex = re.compile("^Withdraw application.*")
        self.base_parser.relevant_income_regex = re.compile("(^Delayed interest.*)|(^Late payment.*)|"
                                                            "(^Interest income.*)|(^Cashback.*)")

        self.base_parser.booking_date = 'Date'
        self.base_parser.booking_date_format = '%Y-%m-%d %H:%M:%S'
        self.base_parser.booking_details = 'Details'
        self.base_parser.booking_id = 'Transaction ID'
        self.base_parser.booking_type = 'Details'
        self.base_parser.booking_value = 'Turnover'

    def test_account_statement_file(self):
        self.assertEqual(os.path.join(os.path.dirname(__file__), 'testdata', 'mintos.csv'),
                         self.base_parser.account_statement_file)

    def test_parse_account_statement(self):
        """test parse_account_statement"""
        expected_statement = [
            {'Datum': datetime.date(2018, 1, 17),
             'Notiz': '236659674: Incoming client payment',
             'Typ': 'Einlage',
             'Wert': '20'},
            {'Datum': datetime.date(2018, 1, 18),
             'Notiz': '237974500: Interest income Loan ID: 2049443-01',
             'Typ': 'Zinsen',
             'Wert': '0,005555556'},
            {'Datum': datetime.date(2018, 1, 19),
             'Notiz': '238112163: Interest income on rebuy Rebuy purpose: agreement_amendment Loan ID: 2198495-01',
             'Typ': 'Zinsen',
             'Wert': '0,003777778'},
            {'Datum': datetime.date(2018, 1, 19),
             'Notiz': '238112984: Interest income on rebuy Rebuy purpose: early_repayment Loan ID: 2202538-01',
             'Typ': 'Zinsen',
             'Wert': '0,003083333'},
            {'Datum': datetime.date(2018, 1, 25),
             'Notiz': '241699935: Late payment fee income Loan ID: 1529173-01',
             'Typ': 'Zinsen',
             'Wert': '0,001214211'},
            {'Datum': datetime.date(2018, 1, 29),
             'Notiz': '243559685: Delayed interest income on rebuy Rebuy purpose: '
                      'agreement_amendment Loan ID: 2198503-01',
             'Typ': 'Zinsen',
             'Wert': '0,000342077'},
            {'Datum': datetime.date(2018, 2, 27),
             'Notiz': '260918485: Cashback bonus',
             'Typ': 'Zinsen',
             'Wert': '0,3'},
            {'Datum': datetime.date(2016, 9, 28),
             'Notiz': '115013710: Withdraw application',
             'Typ': 'Entnahme',
             'Wert': '-20'}]

        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())

    def test_no_statement_file(self):
        """test parse_account_statement with non existent file"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), 'not_existing.csv')
        self.assertFalse(self.base_parser.parse_account_statement())
