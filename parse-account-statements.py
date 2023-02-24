#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An application to read account statement files from different peer to peer lending sites, e.g. Mintos.com and creates
a Portfolio Performance readable csv file.

NOTE: The output only contains interest and interest like payments received. No other statements are currently parsed.

List of currently supported providers:
    - Bondora
    - Bondora Grow Go
    - Estateguru
    - Mintos
    - Robocash
    - Swaper
    - Debitum Network
    - Viainvest

Control the way how account statements are processed via the aggregate parameter:
    - transaction: Currently does not process the input data beyond making it Portfolio Performance compatible.
    - daily: This aggregates all bookings of the same type into one statement per type and day.
    - monthly: This aggregates all bookings of the same type into one statement per type and month. Sets
            the last day of the month as transaction date.

Default behaviour for now is 'transaction'.

Copyright 2018-03-17 ChrisRBe
"""
import argparse
import logging
import os
import sys

from src import p2p_statement_parser
from src import portfolio_writer


root_logger = logging.getLogger()
logger = logging.getLogger("parse-account-statements")


def setup_logging(loglevel=logging.INFO):
    """
    Configure the logging module for this app.
    """
    log_format = "%(asctime)s %(name)-30s %(levelname)-8s %(message)s"
    root_logger.setLevel(loglevel)

    stdout_hdlr = logging.StreamHandler(stream=sys.stdout)
    stdout_hdlr.setFormatter(logging.Formatter(log_format))
    stdout_hdlr.setLevel(loglevel)
    root_logger.addHandler(stdout_hdlr)


def parse_args():
    """
    Parse command line arguments

    :return: list of parsed command line arguments
    """
    arg_parser = argparse.ArgumentParser(
        usage=__doc__,
    )
    arg_parser.add_argument(
        "infile",
        type=str,
        help="CSV file containing the downloaded data from the P2P site",
    )
    arg_parser.add_argument(
        "--aggregate",
        type=str,
        help="specify how account statements should be summarized",
        choices=["transaction", "daily", "monthly"],
        default="transaction",
    )
    arg_parser.add_argument(
        "--type",
        type=str,
        help="Specifies the p2p lending operator",
        choices=[
            "bondora_go_grow",
            "bondora",
            "debitumnetwork",
            "estateguru",
            "mintos",
            "robocash",
            "swaper",
            "lande",
            "viainvest",
            "estateguru_en",
        ],
        default="mintos",
    )
    arg_parser.add_argument(
        "--debug",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
        help="enables debug level logging if set",
    )

    return arg_parser.parse_args()


def platform_factory(infile, operator_name="mintos"):
    """
    Return an object for the required Peer-to-Peer lending platform

    :param operator_name: name of the P2P lending site, defaults to Mintos

    :return: object for the actual lending platform parser, None if not supported
    """
    logger.info("Loading config for %s", operator_name)
    config = os.path.join(os.path.dirname(__file__), "config", f"{operator_name}.yml")
    if os.path.exists(config):
        platform_parser = p2p_statement_parser.PeerToPeerPlatformParser(config, infile)
        return platform_parser
    else:
        logging.error("The provided platform %s is currently not supported", operator_name)
        return None


def main():
    """
    Processes the provided input file with the rules defined for the given platform.
    Outputs a CSV file readable by Portfolio Performance

    :return: True, False if an error occurred.
    """
    options = parse_args()

    setup_logging(loglevel=options.loglevel)

    infile = options.infile
    p2p_operator_name = options.type
    aggregate = options.aggregate

    logger.info("Parsing peer to peer lending site account statements with the following options:")
    logger.info("Account statement file: %s", infile)
    logger.info("Peer to peer platform: %s", p2p_operator_name.upper())
    logger.info("Aggregation type: %s", aggregate.upper())

    if not os.path.exists(infile):
        logger.error("provided file %s does not exist", infile)
        return False

    platform_parser = platform_factory(infile, p2p_operator_name)
    if not platform_parser:
        return False

    statement_list = platform_parser.parse_account_statement(aggregate=aggregate)

    if not statement_list:
        logger.warning(
            "No statements were found in the input file. Re-run with --debug to check for any unexpected statements"
        )
        return False

    logger.info("Account statement parsing finished. Found (and aggregated) %s transactions", len(statement_list))
    logger.info("Writing Portfolio Performance compatible CSV file.")

    writer = portfolio_writer.PortfolioPerformanceWriter()
    writer.init_output()
    for entry in statement_list:
        writer.update_output(entry)
    writer.write_pp_csv_file(
        os.path.join(
            os.path.dirname(infile),
            f"portfolio_performance__{p2p_operator_name}.csv",
        )
    )
    return True


if __name__ == "__main__":
    sys.exit(main())
