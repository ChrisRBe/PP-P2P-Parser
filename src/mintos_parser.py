# -*- coding: utf-8 -*-
"""
Module for the Mintos account statement parser

Copyright 2018-04-29 ChrisRBe
"""
import os

from .p2p_account_statement_parser import PeerToPeerPlatformParser


class MintosParser(PeerToPeerPlatformParser):
    """
    Implementation for the Mintos account statement parser
    """
    def __init__(self):
        """
        Constructor for MintosParser
        """
        super().__init__()

        self.config_file = os.path.join(os.path.dirname(__file__), os.pardir, 'config', 'mintos.yml')
