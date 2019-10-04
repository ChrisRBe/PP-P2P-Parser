# -*- coding: utf-8 -*-
"""
Unit test for the p2p account statement parser module

Copyright 2018-05-01 ChrisRBe
"""
import datetime
import os
from unittest import TestCase

from ..p2p_account_statement_parser import PeerToPeerPlatformParser


class TestBaseParser(TestCase):
    """Test case implementation for PeerToPeerPlatformParser"""
    def setUp(self):
        """test case setUp, run for each test case"""
        self.base_parser = PeerToPeerPlatformParser()
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), 'testdata', 'mintos.csv')
        self.base_parser.config_file = os.path.join(os.path.dirname(__file__),
                                                    os.pardir,
                                                    os.pardir,
                                                    'config',
                                                    'mintos.yml')
        self.maxDiff = None

    def test_account_statement_file(self):
        """test account statement file property"""
        self.assertEqual(os.path.join(os.path.dirname(__file__), 'testdata', 'mintos.csv'),
                         self.base_parser.account_statement_file)

    def test_config_file(self):
        """test config file property"""
        self.assertEqual(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'config', 'mintos.yml'),
                         self.base_parser.config_file)

    def test_bondora_parsing(self):
        """test parse_account_statement for bondora"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), 'testdata', 'bondora.csv')
        self.base_parser.config_file = os.path.join(os.path.dirname(__file__),
                                                    os.pardir,
                                                    os.pardir,
                                                    'config',
                                                    'bondora.yml')
        expected_statement = [{'Datum': datetime.date(2019, 1, 1),
                               'Notiz': ': TransferDeposit|DE1111000000111111',
                               'Typ': 'Einlage',
                               'Wert': '100',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2019, 1, 2),
                               'Notiz': ': TransferGoGrow',
                               'Typ': 'Entnahme',
                               'Wert': '-100',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2019, 1, 3),
                               'Notiz': ': TransferDeposit|Wirecard',
                               'Typ': 'Einlage',
                               'Wert': '100',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2019, 1, 4),
                               'Notiz': '1111111-111111112: TransferInterestRepaiment',
                               'Typ': 'Zinsen',
                               'Wert': '0,0067920792',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2019, 1, 5),
                               'Notiz': '1111111-111111113: TransferExtraInterestRepaiment',
                               'Typ': 'Zinsen',
                               'Wert': '7,05883E-05',
                               'Buchungswährung': 'EUR'}]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())

    def test_bondora_go_grow_parsing(self):
        """test parse_account_statement for bondora"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), 'testdata', 'bondora.csv')
        self.base_parser.config_file = os.path.join(os.path.dirname(__file__),
                                                    os.pardir,
                                                    os.pardir,
                                                    'config',
                                                    'bondora_go_grow.yml')
        expected_statement = [{'Datum': datetime.date(2019, 1, 2),
                               'Notiz': ': TransferGoGrow',
                               'Typ': 'Einlage',
                               'Wert': '-100',
                               'Buchungswährung': 'EUR'}]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())

    def test_estateguru_parsing(self):
        """test parse_account_statement for estateguru"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), 'testdata', 'estateguru.csv')
        self.base_parser.config_file = os.path.join(os.path.dirname(__file__),
                                                    os.pardir,
                                                    os.pardir,
                                                    'config',
                                                    'estateguru.yml')
        expected_statement = [{'Datum': datetime.date(2018, 1, 18),
                               'Notiz': '18012018204714DEP: ',
                               'Typ': 'Einlage',
                               'Wert': '1000,0',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2018, 1, 23),
                               'Notiz': '23012018092020DEP: ',
                               'Typ': 'Einlage',
                               'Wert': '1000,0',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2018, 1, 24),
                               'Notiz': '24012018000000REFEE5975: Kaerepere business loan 2. stage',
                               'Typ': 'Zinsen',
                               'Wert': '0,25',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2018, 1, 24),
                               'Notiz': '24012018000346WIT: ',
                               'Typ': 'Entnahme',
                               'Wert': '-1000,0',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2018, 1, 30),
                               'Notiz': '30012018000000REFEE4182: Laiamäe bridge loan',
                               'Typ': 'Zinsen',
                               'Wert': '0,5',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2018, 2, 24),
                               'Notiz': '24022018000000INTEE5975: Kaerepere business loan 2. stage',
                               'Typ': 'Zinsen',
                               'Wert': '0,46',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2018, 2, 27),
                               'Notiz': '27022018225240DEP: ',
                               'Typ': 'Einlage',
                               'Wert': '1000,0',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2018, 3, 1),
                               'Notiz': '01032018000000BONLT2293: Grevitas construction loan',
                               'Typ': 'Zinsen',
                               'Wert': '0,47',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2018, 3, 15),
                               'Notiz': '15032018000000INTLT0689: Užutekio bridge loan',
                               'Typ': 'Zinsen',
                               'Wert': '0,59',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2018, 4, 8),
                               'Notiz': '08042018000000INTEE3186: Pärnaõie st bridge loan',
                               'Typ': 'Zinsen',
                               'Wert': '0,46',
                               'Buchungswährung': 'EUR'}]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())

    def test_mintos_parsing(self):
        """test parse_account_statement for mintos"""
        expected_statement = [
            {'Datum': datetime.date(2018, 1, 17),
             'Notiz': '236659674: Incoming client payment',
             'Typ': 'Einlage',
             'Wert': '20',
             'Buchungswährung': 'EUR'},
            {'Datum': datetime.date(2018, 1, 18),
             'Notiz': '237974500: Interest income Loan ID: 2049443-01',
             'Typ': 'Zinsen',
             'Wert': '0,005555556',
             'Buchungswährung': 'EUR'},
            {'Datum': datetime.date(2018, 1, 19),
             'Notiz': '238112163: Interest income on rebuy Rebuy purpose: agreement_amendment Loan ID: 2198495-01',
             'Typ': 'Zinsen',
             'Wert': '0,003777778',
             'Buchungswährung': 'EUR'},
            {'Datum': datetime.date(2018, 1, 19),
             'Notiz': '238112984: Interest income on rebuy Rebuy purpose: early_repayment Loan ID: 2202538-01',
             'Typ': 'Zinsen',
             'Wert': '0,003083333',
             'Buchungswährung': 'EUR'},
            {'Datum': datetime.date(2018, 1, 25),
             'Notiz': '241699935: Late payment fee income Loan ID: 1529173-01',
             'Typ': 'Zinsen',
             'Wert': '0,001214211',
             'Buchungswährung': 'EUR'},
            {'Datum': datetime.date(2018, 1, 29),
             'Notiz': '243559685: Delayed interest income on rebuy Rebuy purpose: '
                      'agreement_amendment Loan ID: 2198503-01',
             'Typ': 'Zinsen',
             'Wert': '0,000342077',
             'Buchungswährung': 'EUR'},
            {'Datum': datetime.date(2018, 2, 27),
             'Notiz': '260918485: Cashback bonus',
             'Typ': 'Zinsen',
             'Wert': '0,3',
             'Buchungswährung': 'EUR'},
            {'Datum': datetime.date(2016, 9, 28),
             'Notiz': '115013710: Withdraw application',
             'Typ': 'Entnahme',
             'Wert': '-20',
             'Buchungswährung': 'EUR'}]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())

    def test_no_statement_file(self):
        """test parse_account_statement with non existent file"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), 'not_existing.csv')
        self.assertFalse(self.base_parser.parse_account_statement())

    def test_robocash_parsing(self):
        """test parse_account_statement for robocash"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), 'testdata', 'robocash.csv')
        self.base_parser.config_file = os.path.join(os.path.dirname(__file__),
                                                    os.pardir,
                                                    os.pardir,
                                                    'config',
                                                    'robocash.yml')
        expected_statement = [{'Datum': datetime.date(2018, 2, 15),
                               'Notiz': '2438244: ',
                               'Typ': 'Einlage',
                               'Wert': '2000',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2018, 2, 16),
                               'Notiz': '2458795: 856836',
                               'Typ': 'Zinsen',
                               'Wert': '0,003835616',
                               'Buchungswährung': 'EUR'}]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())

    def test_swaper_parsing(self):
        """test parse_account_statement for swaper"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), 'testdata', 'swaper.csv')
        self.base_parser.config_file = os.path.join(os.path.dirname(__file__),
                                                    os.pardir,
                                                    os.pardir,
                                                    'config',
                                                    'swaper.yml')
        expected_statement = [{'Datum': datetime.date(2018, 5, 1),
                               'Notiz': 'PL-84587: 119113',
                               'Typ': 'Zinsen',
                               'Wert': '0,1',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2018, 4, 30),
                               'Notiz': 'PL-82794: 116800',
                               'Typ': 'Zinsen',
                               'Wert': '0,12',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2018, 4, 26),
                               'Notiz': 'GL-22989301: 117251',
                               'Typ': 'Zinsen',
                               'Wert': '0,11',
                               'Buchungswährung': 'EUR'},
                              {'Datum': datetime.date(2018, 1, 24),
                               'Notiz': ': ',
                               'Typ': 'Einlage',
                               'Wert': '2000',
                               'Buchungswährung': 'EUR'}]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())
