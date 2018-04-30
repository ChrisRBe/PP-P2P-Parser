# -*- coding: utf-8 -*-
"""
Unit test for the mintos parser module

Copyright 2018-04-29 ChrisRBe
"""
import datetime
import os
from unittest import TestCase

from ..mintos_parser import MintosParser


class TestMintosParser(TestCase):
    """Test case implementation for MintosParser"""

    def setUp(self):
        """test case setUp, run for each test case"""
        self.mintos = MintosParser()
        self.mintos.account_statement_file = os.path.join(os.path.dirname(__file__), 'testdata', 'mintos.csv')

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
             'Wert': '0,3'}]

        self.assertEqual(expected_statement, self.mintos.parse_account_statement())
