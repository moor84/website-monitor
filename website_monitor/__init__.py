"""
Website availability monitor that works with Aiven services.

Copyright (c) 2021 Mikhail Medvedev
"""
import argparse
import logging

from website_monitor.config import init_config_file


log = logging.getLogger()


def init_logger():
    """Initialise the logging subsystem"""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(f'[%(asctime)s] %(name)s level=%(levelname)s %(filename)s:%(lineno)d "%(message)s"')
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Silencing the noisy Kafka logger
    kafka_logger = logging.getLogger('kafka')
    kafka_logger.setLevel(logging.ERROR)


def main():
    """Application's main function"""
    parser = argparse.ArgumentParser(description='hey now')
    parser.add_argument(dest='command', choices=['checker', 'writer'])
    parser.add_argument('-c', '--config', type=str, dest='config_file', required=True)
    parser.add_argument('-u', '--url', type=str, dest='url')
    parser.add_argument('-p', '--pattern', type=str, dest='pattern')
    args = parser.parse_args()

    init_config_file(args.config_file)
    init_logger()
    
    if args.command == 'checker':
        if not args.url:
            print('Please pass the url for checker')
            return
        from website_monitor.checker import run_checker
        run_checker(args.url, args.pattern)
    elif args.command == 'writer':
        from website_monitor.writer import run_writer
        run_writer()
