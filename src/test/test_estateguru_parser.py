# -*- coding: utf-8 -*-
"""
Unit test for the estateguru parser module

Copyright 2018-04-30 ChrisRBe
"""
import datetime
import os
from unittest import TestCase

from ..estateguru_parser import EstateguruParser


class TestEstateguruParser(TestCase):
    """Test case implementation for MintosParser"""
    def setUp(self):
        """test case setUp, run for each test case"""
        self.eguru = EstateguruParser()
        self.eguru.account_statement_file = os.path.join(os.path.dirname(__file__), 'testdata', 'estateguru.csv')

    def test_parse_account_statement(self):
        """test parse_account_statement"""
        expected_statement = [{'Datum': datetime.date(2018, 1, 18),
                               'Notiz': '18012018204714DEP: ',
                               'Typ': 'Einlage',
                               'Wert': '1000,0'},
                              {'Datum': datetime.date(2018, 1, 23),
                               'Notiz': '23012018092020DEP: ',
                               'Typ': 'Einlage',
                               'Wert': '1000,0'},
                              {'Datum': datetime.date(2018, 1, 24),
                               'Notiz': '24012018000000REFEE5975: Kaerepere business loan 2. stage',
                               'Typ': 'Zinsen',
                               'Wert': '0,25'},
                              {'Datum': datetime.date(2018, 1, 24),
                               'Notiz': '24012018000346WIT: ',
                               'Typ': 'Entnahme',
                               'Wert': '-1000,0'},
                              {'Datum': datetime.date(2018, 1, 30),
                               'Notiz': '30012018000000REFEE4182: Laiamäe bridge loan',
                               'Typ': 'Zinsen',
                               'Wert': '0,5'},
                              {'Datum': datetime.date(2018, 2, 24),
                               'Notiz': '24022018000000INTEE5975: Kaerepere business loan 2. stage',
                               'Typ': 'Zinsen',
                               'Wert': '0,46'},
                              {'Datum': datetime.date(2018, 2, 27),
                               'Notiz': '27022018225240DEP: ',
                               'Typ': 'Einlage',
                               'Wert': '1000,0'},
                              {'Datum': datetime.date(2018, 3, 1),
                               'Notiz': '01032018000000BONLT2293: Grevitas construction loan',
                               'Typ': 'Zinsen',
                               'Wert': '0,47'},
                              {'Datum': datetime.date(2018, 3, 15),
                               'Notiz': '15032018000000INTLT0689: Užutekio bridge loan',
                               'Typ': 'Zinsen',
                               'Wert': '0,59'},
                              {'Datum': datetime.date(2018, 4, 8),
                               'Notiz': '08042018000000INTEE3186: Pärnaõie st bridge loan',
                               'Typ': 'Zinsen',
                               'Wert': '0,46'}]
        self.assertEqual(expected_statement, self.eguru.parse_account_statement())
