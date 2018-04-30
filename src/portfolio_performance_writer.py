# -*- coding: utf-8 -*-
"""
Module for the portfolio performance writer

Copyright 2018-04-29 ChrisRBe
"""
import codecs
import csv
import io
import logging

PP_FIELDNAMES = ['Datum', 'Wert', 'Typ', 'Notiz']


class PortfolioPerformanceWriter(object):
    """
    Writing parsed Peer-to-Peer lending account statements to Portfolio Performance compatible format
    """
    def __init__(self, dialect='excel'):
        """
        constructor for class

        :param dialect: translates to the used CSV dialect, defaults to excel
        """
        self.dialect = dialect
        self.out_csv_fieldnames = PP_FIELDNAMES
        self.out_string_stream = io.StringIO()
        self.out_csv_writer = None

    def init_output(self):
        """
        Initialize output csv file

        :return:
        """
        if not self.out_csv_writer:
            self.out_csv_writer = csv.DictWriter(f=self.out_string_stream,
                                                 fieldnames=self.out_csv_fieldnames,
                                                 dialect=self.dialect)
            self.out_csv_writer.writeheader()

    def update_output(self, statement_dict):
        """
        Add a new line to the portfolio performance output file; format is a dictionary

        :param statement_dict: dictionary containing the fieldnames of the output file and the respective content as
        key value pair
        :return:
        """
        if statement_dict:
            self.out_csv_writer.writerow(statement_dict)

    def write_pp_csv_file(self, outfile='portfolio_performance.csv'):
        """
        Write the content of the complete string stream into the actual output file.
        Should be called after the parsed account statement has been written to the stream.

        :param outfile: specifies the path and name of the output file, defaults to portfolio_performance.csv
        :return:
        """
        with codecs.open(outfile, 'w', encoding='utf-8') as csv_output:
            stream_content = self.out_string_stream.getvalue()
            logging.debug(stream_content)
            csv_output.write(stream_content.strip())
