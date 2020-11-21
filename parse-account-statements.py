#!/usr/bin/python3
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

Control the way how account statements are processed via the aggregate parameter:
    - daily: Currently does not process the input data beyond making it Portfolio Performance compatible.
    - monthly: This aggregates all bookings of the same type into one statement per type and month. Sets
            the last day of the month as transaction date.

Default behaviour for now is 'daily'.

Copyright 2018-03-17 ChrisRBe
"""
import argparse
import logging
import os
import sys

from src import p2p_account_statement_parser
from src import portfolio_performance_writer


def platform_factory(infile, operator_name="mintos"):
    """
    Return an object for the required Peer-to-Peer lending platform

    :param operator_name: name of the P2P lending site, defaults to Mintos

    :return: object for the actual lending platform parser, None if not supported
    """
    config = os.path.join(os.path.dirname(__file__), "config", "{op}.yml".format(op=operator_name))
    if os.path.exists(config):
        platform_parser = p2p_account_statement_parser.PeerToPeerPlatformParser(config, infile)
        return platform_parser
    else:
        logging.error("The provided platform {} is currently not supported".format(operator_name))
        return None


def main(infile, p2p_operator_name="mintos", aggregate="daily"):
    """
    Processes the provided input file with the rules defined for the given platform.
    Outputs a CSV file readable by Portfolio Performance

    :param infile: input file containing the account statements from a supported platform
    :param p2p_operator_name: name of the Peer-to-Peer lending platform, defaults to Mintos
    :param aggregate: specifies the aggregation period. defaults to daily.

    :return: True, False if an error occurred.
    """
    if not os.path.exists(infile):
        logging.error("provided file {} does not exist".format(infile))
        return False

    platform_parser = platform_factory(infile, p2p_operator_name)
    if not platform_parser:
        return False

    statement_list = platform_parser.parse_account_statement(aggregate=aggregate)

    if not statement_list:
        return False

    writer = portfolio_performance_writer.PortfolioPerformanceWriter()
    writer.init_output()
    for entry in statement_list:
        writer.update_output(entry)
    writer.write_pp_csv_file(
        os.path.join(
            os.path.dirname(infile),
            "portfolio_performance__{}.csv".format(p2p_operator_name),
        )
    )
    return True


if __name__ == "__main__":
    ARG_PARSER = argparse.ArgumentParser(
        usage=__doc__,
    )
    ARG_PARSER.add_argument(
        "infile",
        type=str,
        help="CSV file containing the downloaded data from the P2P site",
    )
    ARG_PARSER.add_argument(
        "--aggregate",
        type=str,
        help="specify how account statements should be summarized",
        choices=["daily", "monthly"],
        default="daily",
    )
    ARG_PARSER.add_argument("--type", type=str, help="Specifies the p2p lending operator")
    ARG_PARSER.add_argument("--debug", action="store_true", help="enables debug level logging if set")

    CMD_ARGS = ARG_PARSER.parse_args()

    if CMD_ARGS.debug:
        logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

    sys.exit(main(CMD_ARGS.infile, CMD_ARGS.type, CMD_ARGS.aggregate))
