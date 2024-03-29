# -*- coding: utf-8 -*-
"""
Unit test for the p2p account statement parser module

Copyright 2018-05-01 ChrisRBe
"""
import datetime
import os
import unittest

from src.p2p_statement_parser import PeerToPeerPlatformParser


class TestBaseParser(unittest.TestCase):
    """Test case implementation for PeerToPeerPlatformParser"""

    def setUp(self):
        """test case setUp, run for each test case"""
        self.account_statement_file = os.path.join(os.path.dirname(__file__), "testdata", "mintos.csv")
        self.config_file = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "config", "mintos.yml")
        self.base_parser = PeerToPeerPlatformParser(infile=self.account_statement_file, config=self.config_file)
        self.maxDiff = None

    def test_account_statement_file(self):
        """test account statement file property"""
        self.assertEqual(
            os.path.join(os.path.dirname(__file__), "testdata", "mintos.csv"),
            self.base_parser.account_statement_file,
        )

    def test_config_file(self):
        """test config file property"""
        self.assertEqual(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "config", "mintos.yml"),
            self.base_parser.config_file,
        )

    def test_bondora_parsing(self):
        """test parse_account_statement for bondora"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), "testdata", "bondora.csv")
        self.base_parser.config_file = os.path.join(
            os.path.dirname(__file__), os.pardir, os.pardir, "config", "bondora.yml"
        )
        expected_statement = [
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2019, 1, 1),
                "Notiz": ": TransferDeposit|DE1111000000111111",
                "Typ": "Einlage",
                "Wert": 100.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2019, 1, 2),
                "Notiz": ": TransferGoGrow",
                "Typ": "Entnahme",
                "Wert": -100.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2019, 1, 3),
                "Notiz": ": TransferDeposit|Wirecard",
                "Typ": "Einlage",
                "Wert": 100.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2019, 1, 4),
                "Notiz": "1111111-111111112: TransferInterestRepaiment",
                "Typ": "Zinsen",
                "Wert": 0.006792079,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2019, 1, 5),
                "Notiz": "1111111-111111113: TransferExtraInterestRepaiment",
                "Typ": "Zinsen",
                "Wert": 7.0588e-05,
            },
        ]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())

    def test_bondora_go_grow_parsing(self):
        """test parse_account_statement for bondora"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), "testdata", "bondora.csv")
        self.base_parser.config_file = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            "config",
            "bondora_go_grow.yml",
        )
        expected_statement = [
            {
                "Datum": datetime.date(2019, 1, 2),
                "Notiz": ": TransferGoGrow",
                "Typ": "Einlage",
                "Wert": -100.0,
                "Buchungswährung": "EUR",
            }
        ]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())

    def test_estateguru_parsing(self):
        """test parse_account_statement for estateguru"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), "testdata", "estateguru.csv")
        self.base_parser.config_file = os.path.join(
            os.path.dirname(__file__), os.pardir, os.pardir, "config", "estateguru.yml"
        )
        expected_statement = [
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 18),
                "Notiz": "18012018204714DEP: ",
                "Typ": "Einlage",
                "Wert": 1000.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 23),
                "Notiz": "23012018092020DEP: ",
                "Typ": "Einlage",
                "Wert": 1000.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 24),
                "Notiz": "24012018000000REFEE5975: Kaerepere business loan 2. stage",
                "Typ": "Zinsen",
                "Wert": 0.25,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 24),
                "Notiz": "24012018000346WIT: ",
                "Typ": "Entnahme",
                "Wert": -1000.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 30),
                "Notiz": "30012018000000REFEE4182: Laiamäe bridge loan",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 2, 24),
                "Notiz": "24022018000000INTEE5975: Kaerepere business loan 2. stage",
                "Typ": "Zinsen",
                "Wert": 0.46,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 2, 27),
                "Notiz": "27022018225240DEP: ",
                "Typ": "Einlage",
                "Wert": 1000.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 3, 1),
                "Notiz": "01032018000000BONLT2293: Grevitas construction loan",
                "Typ": "Zinsen",
                "Wert": 0.47,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 3, 15),
                "Notiz": "15032018000000INTLT0689: Užutekio bridge loan",
                "Typ": "Zinsen",
                "Wert": 0.59,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 4, 8),
                "Notiz": "08042018000000INTEE3186: Pärnaõie st bridge loan",
                "Typ": "Zinsen",
                "Wert": 0.46,
            },
        ]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())

    def test_mintos_parsing(self):
        """test parse_account_statement for mintos"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), "testdata", "mintos.csv")
        self.base_parser.config_file = os.path.join(
            os.path.dirname(__file__), os.pardir, os.pardir, "config", "mintos.yml"
        )
        expected_statement = [
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 17),
                "Notiz": "236659674: Incoming client payment",
                "Typ": "Einlage",
                "Wert": 20.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 18),
                "Notiz": "237974500: Interest income Loan ID: 2049443-01",
                "Typ": "Zinsen",
                "Wert": 0.005555556,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 19),
                "Notiz": "238112163: Interest income on rebuy Rebuy purpose: "
                "agreement_amendment Loan ID: 2198495-01",
                "Typ": "Zinsen",
                "Wert": 0.003777778,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 19),
                "Notiz": "238112984: Interest income on rebuy Rebuy purpose: early_repayment " "Loan ID: 2202538-01",
                "Typ": "Zinsen",
                "Wert": 0.003083333,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 25),
                "Notiz": "241699935: Late payment fee income Loan ID: 1529173-01",
                "Typ": "Zinsen",
                "Wert": 0.001214211,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 29),
                "Notiz": "243559685: Delayed interest income on rebuy Rebuy purpose: "
                "agreement_amendment Loan ID: 2198503-01",
                "Typ": "Zinsen",
                "Wert": 0.000342077,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 2, 27),
                "Notiz": "260918485: Cashback bonus",
                "Typ": "Zinsen",
                "Wert": 0.3,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2016, 9, 28),
                "Notiz": "115013710: Withdraw application",
                "Typ": "Entnahme",
                "Wert": -20.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2020, 4, 10),
                "Notiz": "178363724: Loan 28375000-01 - discount/premium for secondary market transaction 178363274.",
                "Typ": "Gebühren",
                "Wert": -0.145454545,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2020, 4, 10),
                "Notiz": "178363725: Loan 28375000-01 - discount/premium for secondary market transaction 178363275.",
                "Typ": "Zinsen",
                "Wert": 0.505454545,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(1970, 1, 1),
                "Notiz": "127373922: Loan 35287609-01 - interest received (no date for testing)",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
        ]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())

    def test_mintos_parsing_daily_aggregation(self):
        """test parse_account_statement for mintos"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), "testdata", "mintos.csv")
        self.base_parser.config_file = os.path.join(
            os.path.dirname(__file__), os.pardir, os.pardir, "config", "mintos.yml"
        )
        expected_statement = [
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 17),
                "Notiz": "Tageszusammenfassung",
                "Typ": "Einlage",
                "Wert": 20.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 18),
                "Notiz": "Tageszusammenfassung",
                "Typ": "Zinsen",
                "Wert": 0.005555556,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 19),
                "Notiz": "Tageszusammenfassung",
                "Typ": "Zinsen",
                "Wert": 0.006861111,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 25),
                "Notiz": "Tageszusammenfassung",
                "Typ": "Zinsen",
                "Wert": 0.001214211,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 29),
                "Notiz": "Tageszusammenfassung",
                "Typ": "Zinsen",
                "Wert": 0.000342077,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 2, 27),
                "Notiz": "Tageszusammenfassung",
                "Typ": "Zinsen",
                "Wert": 0.3,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2016, 9, 28),
                "Notiz": "Tageszusammenfassung",
                "Typ": "Entnahme",
                "Wert": -20.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2020, 4, 10),
                "Notiz": "Tageszusammenfassung",
                "Typ": "Gebühren",
                "Wert": -0.145454545,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2020, 4, 10),
                "Notiz": "Tageszusammenfassung",
                "Typ": "Zinsen",
                "Wert": 0.505454545,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(1970, 1, 1),
                "Notiz": "Tageszusammenfassung",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
        ]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement(aggregate="daily"))

    def test_mintos_parsing_transaction_aggregation(self):
        """test parse_account_statement for mintos"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), "testdata", "mintos.csv")
        self.base_parser.config_file = os.path.join(
            os.path.dirname(__file__), os.pardir, os.pardir, "config", "mintos.yml"
        )
        expected_statement = [
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 17),
                "Notiz": "236659674: Incoming client payment",
                "Typ": "Einlage",
                "Wert": 20.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 18),
                "Notiz": "237974500: Interest income Loan ID: 2049443-01",
                "Typ": "Zinsen",
                "Wert": 0.005555556,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 19),
                "Notiz": "238112163: Interest income on rebuy Rebuy purpose: "
                "agreement_amendment Loan ID: 2198495-01",
                "Typ": "Zinsen",
                "Wert": 0.003777778,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 19),
                "Notiz": "238112984: Interest income on rebuy Rebuy purpose: early_repayment " "Loan ID: 2202538-01",
                "Typ": "Zinsen",
                "Wert": 0.003083333,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 25),
                "Notiz": "241699935: Late payment fee income Loan ID: 1529173-01",
                "Typ": "Zinsen",
                "Wert": 0.001214211,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 29),
                "Notiz": "243559685: Delayed interest income on rebuy Rebuy purpose: "
                "agreement_amendment Loan ID: 2198503-01",
                "Typ": "Zinsen",
                "Wert": 0.000342077,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 2, 27),
                "Notiz": "260918485: Cashback bonus",
                "Typ": "Zinsen",
                "Wert": 0.3,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2016, 9, 28),
                "Notiz": "115013710: Withdraw application",
                "Typ": "Entnahme",
                "Wert": -20.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2020, 4, 10),
                "Notiz": "178363724: Loan 28375000-01 - discount/premium for secondary market transaction 178363274.",
                "Typ": "Gebühren",
                "Wert": -0.145454545,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2020, 4, 10),
                "Notiz": "178363725: Loan 28375000-01 - discount/premium for secondary market transaction 178363275.",
                "Typ": "Zinsen",
                "Wert": 0.505454545,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(1970, 1, 1),
                "Notiz": "127373922: Loan 35287609-01 - interest received (no date for testing)",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
        ]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement(aggregate="transaction"))

    def test_mintos_parsing_monthly_aggregation(self):
        """test parse_account_statement for mintos"""
        self.base_parser.account_statement_file = os.path.join(
            os.path.dirname(__file__), "testdata", "mintos_several_months.csv"
        )
        self.base_parser.config_file = os.path.join(
            os.path.dirname(__file__), os.pardir, os.pardir, "config", "mintos.yml"
        )
        expected_statement = [
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 2, 28),
                "Notiz": "Monatszusammenfassung",
                "Typ": "Einlage",
                "Wert": 20.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 2, 28),
                "Notiz": "Monatszusammenfassung",
                "Typ": "Zinsen",
                "Wert": 0.3,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 31),
                "Notiz": "Monatszusammenfassung",
                "Typ": "Einlage",
                "Wert": 20.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 31),
                "Notiz": "Monatszusammenfassung",
                "Typ": "Zinsen",
                "Wert": 0.013972955,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2016, 9, 30),
                "Notiz": "Monatszusammenfassung",
                "Typ": "Entnahme",
                "Wert": -20.0,
            },
        ]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement(aggregate="monthly"))

    def test_viainvest_parsing_transaction_aggregation(self):
        """test parse_account_statement for viainvest"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), "testdata", "viainvest.csv")
        self.base_parser.config_file = os.path.join(
            os.path.dirname(__file__), os.pardir, os.pardir, "config", "viainvest.yml"
        )
        expected_statement = [
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2020, 12, 13),
                "Notiz": ": ",
                "Typ": "Einlage",
                "Wert": 1000.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2020, 12, 14),
                "Notiz": "04-1246342: 04-1246342",
                "Typ": "Zinsen",
                "Wert": 0.10,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2020, 12, 14),
                "Notiz": "05-3233341: 05-3233341",
                "Typ": "Zinsen",
                "Wert": 0.09,
            },
        ]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement(aggregate="transaction"))

    @unittest.skip("Currently not checking if infile exists.")
    def test_no_statement_file(self):
        """test parse_account_statement with non existent file"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), "not_existing.csv")
        self.assertFalse(self.base_parser.parse_account_statement())

    def test_robocash_parsing(self):
        """test parse_account_statement for robocash"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), "testdata", "robocash.csv")
        self.base_parser.config_file = os.path.join(
            os.path.dirname(__file__), os.pardir, os.pardir, "config", "robocash.yml"
        )
        expected_statement = [
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 2, 15),
                "Notiz": "2438244: ",
                "Typ": "Einlage",
                "Wert": 2000.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 2, 16),
                "Notiz": "2458795: 856836",
                "Typ": "Zinsen",
                "Wert": 0.003835616,
            },
        ]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())

    def test_swaper_parsing(self):
        """test parse_account_statement for swaper"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), "testdata", "swaper.csv")
        self.base_parser.config_file = os.path.join(
            os.path.dirname(__file__), os.pardir, os.pardir, "config", "swaper.yml"
        )
        expected_statement = [
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 5, 1),
                "Notiz": "PL-84587: 119113",
                "Typ": "Zinsen",
                "Wert": 0.1,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 4, 30),
                "Notiz": "PL-82794: 116800",
                "Typ": "Zinsen",
                "Wert": 0.12,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 4, 26),
                "Notiz": "GL-22989301: 117251",
                "Typ": "Zinsen",
                "Wert": 0.11,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2018, 1, 24),
                "Notiz": ": ",
                "Typ": "Einlage",
                "Wert": 2000.0,
            },
        ]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())

    def test_debitumnetwork_parsing(self):
        """test parse_account_statement for debitum network"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), "testdata", "debitum.csv")
        self.base_parser.config_file = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            "config",
            "debitumnetwork.yml",
        )
        expected_statement = [
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2020, 8, 25),
                "Notiz": "405eea2a-7745-4588-8f08-5c1512987324: NA",
                "Typ": "Einlage",
                "Wert": 121.91,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2020, 9, 7),
                "Notiz": "b9da7662-de61-43d1-a179-c300d5695587: " "6c4a6d93-faea-4d96-856c-7cdd3fb3023b",
                "Typ": "Zinsen",
                "Wert": 10.03,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2020, 9, 7),
                "Notiz": "7260c567-fdb4-44d4-84ce-4256c7d7fb80: NA",
                "Typ": "Einlage",
                "Wert": 10.0,
            },
        ]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())

    def test_lande_parsing(self):
        """test parse_account_statement for lande.finance"""
        self.base_parser.account_statement_file = os.path.join(os.path.dirname(__file__), "testdata", "lande.csv")
        self.base_parser.config_file = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            "config",
            "lande.yml",
        )
        expected_statement = [
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2022, 11, 8),
                "Notiz": "97b1a146-1c3f-47e5-8ac3-10ade56765ec: ",
                "Typ": "Einlage",
                "Wert": 500.0,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2022, 11, 8),
                "Notiz": "97b20fa6-c6cd-4c08-8f4a-b25f120ec583: 221108-366978",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2022, 11, 11),
                "Notiz": "97b7d986-c414-427f-90a2-c05e98641900: 221109-297724",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2022, 11, 11),
                "Notiz": "97b8289e-fd86-4312-84de-f50631fb571f: 221108-142849",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2022, 11, 11),
                "Notiz": "97b833cf-9d9f-4ff2-a800-a2b1ebaea865: 221101-847953",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2022, 11, 14),
                "Notiz": "97be0c4f-a4d1-4e7d-aeff-f07e7c446d7e: 220929-309009",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2022, 11, 14),
                "Notiz": "97be0ca1-0c64-498f-9a47-bc2c7f1ca1ed: 220926-944705",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2022, 11, 14),
                "Notiz": "97be0cfb-3ceb-4bdc-9411-b25acae80a6e: 221011-882308",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2022, 11, 14),
                "Notiz": "97be0d40-9237-4683-a6d9-be836ba90580: 221012-476486",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2022, 11, 14),
                "Notiz": "97be0d93-81a0-428b-9ea3-23be8ff7cfca: 221101-842051",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2022, 11, 14),
                "Notiz": "97be48c7-c79d-4a35-a440-4048b74b17c8: 221114-968949",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
            {
                "Buchungswährung": "EUR",
                "Datum": datetime.date(2022, 12, 1),
                "Notiz": "97e065db-dcad-4a29-8738-5adbfc74fc49: 221011-882308",
                "Typ": "Zinsen",
                "Wert": 0.5,
            },
        ]
        self.assertEqual(expected_statement, self.base_parser.parse_account_statement())

    def test_aggregation_not_supported(self):
        """test if unsopported aggregation is correctly handled"""
        self.assertFalse(self.base_parser.parse_account_statement(aggregate="yearly"))
