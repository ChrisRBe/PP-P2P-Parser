# -*- coding: utf-8 -*-
"""
Module for the Estateguru account statement parser

Copyright 2018-04-30 ChrisRBe
"""
import os

from .p2p_account_statement_parser import PeerToPeerPlatformParser


class EstateguruParser(PeerToPeerPlatformParser):
    """
    Implementation for the Estateguru account statement parser
    """
    def __init__(self):
        """
        Constructor for EstateguruParser
        """
        super().__init__()

        self.config_file = os.path.join(os.path.dirname(__file__), os.pardir, 'config', 'estateguru.yml')
