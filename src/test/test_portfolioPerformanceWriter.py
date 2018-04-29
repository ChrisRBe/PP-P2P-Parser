# Copyright 2018-04-29 ChrisRBe
# -*- coding: utf-8 -*-
import os
import tempfile
from unittest import TestCase

from ..portfolio_performance_writer import PortfolioPerformanceWriter
from ..portfolio_performance_writer import PP_FIELDNAMES


class TestPortfolioPerformanceWriter(TestCase):
    def setUp(self):
        self.p = PortfolioPerformanceWriter()
        self.p.init_output()

    def test_init_output(self):
        self.assertEqual(','.join(PP_FIELDNAMES), self.p.out_string_stream.getvalue().strip())

    def test_update_output(self):
        test_entry = {PP_FIELDNAMES[0]: 'date',
                      PP_FIELDNAMES[1]: 'profit',
                      PP_FIELDNAMES[2]: 'category',
                      PP_FIELDNAMES[3]: 'note'}
        self.p.update_output(test_entry)
        self.assertEqual('Datum,Wert,Typ,Notiz\r\ndate,profit,category,note',
                         self.p.out_string_stream.getvalue().strip())

    def test_write_pp_csv_file(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            fname = os.path.join(tmpdirname, 'output')
            self.p.write_pp_csv_file(fname)
            with open(fname, 'r') as testfile:
                self.assertEqual(','.join(PP_FIELDNAMES), testfile.read().strip())
