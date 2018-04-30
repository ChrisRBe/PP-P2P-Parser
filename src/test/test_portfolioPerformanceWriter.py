# -*- coding: utf-8 -*-
"""
Unit test for the portfolio performance writer module

Copyright 2018-04-29 ChrisRBe
"""
import os
import tempfile
from unittest import TestCase

from ..portfolio_performance_writer import PortfolioPerformanceWriter
from ..portfolio_performance_writer import PP_FIELDNAMES


class TestPortfolioPerformanceWriter(TestCase):
    """Test case implementation for PortfolioPerformanceWriter"""

    def setUp(self):
        """test case setUp, run for each test case"""
        self.pp_writer = PortfolioPerformanceWriter()
        self.pp_writer.init_output()

    def test_init_output(self):
        """test init_output"""
        self.assertEqual(','.join(PP_FIELDNAMES), self.pp_writer.out_string_stream.getvalue().strip())

    def test_update_output(self):
        """test update_output"""
        test_entry = {PP_FIELDNAMES[0]: 'date',
                      PP_FIELDNAMES[1]: 'profit',
                      PP_FIELDNAMES[2]: 'category',
                      PP_FIELDNAMES[3]: 'note'}
        self.pp_writer.update_output(test_entry)
        self.assertEqual('Datum,Wert,Typ,Notiz\r\ndate,profit,category,note',
                         self.pp_writer.out_string_stream.getvalue().strip())

    def test_write_pp_csv_file(self):
        """test write_pp_csv_file"""
        with tempfile.TemporaryDirectory() as tmpdirname:
            fname = os.path.join(tmpdirname, 'output')
            self.pp_writer.write_pp_csv_file(fname)
            with open(fname, 'r') as testfile:
                self.assertEqual(','.join(PP_FIELDNAMES), testfile.read().strip())
