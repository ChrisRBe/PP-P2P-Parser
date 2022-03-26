# -*- coding: utf-8 -*-
"""
Unit test for the portfolio performance writer module

Copyright 2018-04-29 ChrisRBe
"""
import codecs
import locale
import os
import tempfile
from unittest import TestCase

from src.portfolio_writer import PortfolioPerformanceWriter
from src.portfolio_writer import PP_FIELDNAMES


class TestPortfolioPerformanceWriter(TestCase):
    """Test case implementation for PortfolioPerformanceWriter"""

    def setUp(self):
        """test case setUp, run for each test case"""
        self.pp_writer = PortfolioPerformanceWriter()
        self.pp_writer.init_output()

    def test_init_output(self):
        """test init_output"""
        self.assertEqual(",".join(PP_FIELDNAMES), self.pp_writer.out_string_stream.getvalue().strip())

    def test_update_output(self):
        """test update_output"""
        locale.setlocale(locale.LC_ALL, "de_DE.utf-8")
        test_entry = {
            PP_FIELDNAMES[0]: "date",
            PP_FIELDNAMES[1]: 123.456789,
            PP_FIELDNAMES[2]: "currency",
            PP_FIELDNAMES[3]: "category",
            PP_FIELDNAMES[4]: "note",
        }
        self.pp_writer.update_output(test_entry)
        self.assertEqual(
            'Datum,Wert,Buchungswährung,Typ,Notiz\r\ndate,"123,45679",currency,category,note',
            self.pp_writer.out_string_stream.getvalue().strip(),
        )

    def test_update_output_umlaut(self):
        """test update_output with umlauts"""
        locale.setlocale(locale.LC_ALL, "de_DE.utf-8")
        test_entry = {
            PP_FIELDNAMES[0]: "date",
            PP_FIELDNAMES[1]: 0.123456789,
            PP_FIELDNAMES[2]: "currency",
            PP_FIELDNAMES[3]: "category",
            PP_FIELDNAMES[4]: "Laiamäe Pärnaõie Užutekio",
        }
        self.pp_writer.update_output(test_entry)
        self.assertEqual(
            'Datum,Wert,Buchungswährung,Typ,Notiz\r\ndate,"0,12345679",currency,category,Laiamäe Pärnaõie Užutekio',
            self.pp_writer.out_string_stream.getvalue().strip(),
        )

    def test_update_output_umlaut_en_us(self):
        """test update_output with umlauts"""
        locale.setlocale(locale.LC_ALL, "en_US.utf-8")
        test_entry = {
            PP_FIELDNAMES[0]: "date",
            PP_FIELDNAMES[1]: 0.123456789,
            PP_FIELDNAMES[2]: "currency",
            PP_FIELDNAMES[3]: "category",
            PP_FIELDNAMES[4]: "Laiamäe Pärnaõie Užutekio",
        }
        self.pp_writer.update_output(test_entry)
        self.assertEqual(
            "Datum,Wert,Buchungswährung,Typ,Notiz\r\ndate,0.12345679,currency,category,Laiamäe Pärnaõie Užutekio",
            self.pp_writer.out_string_stream.getvalue().strip(),
        )

    def test_write_pp_csv_file(self):
        """test write_pp_csv_file"""
        with tempfile.TemporaryDirectory() as tmpdirname:
            fname = os.path.join(tmpdirname, "output")
            self.pp_writer.write_pp_csv_file(fname)
            with codecs.open(fname, "r", encoding="utf-8") as testfile:
                self.assertEqual(",".join(PP_FIELDNAMES), testfile.read().strip())
