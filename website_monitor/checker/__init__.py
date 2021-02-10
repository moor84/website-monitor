"""
Checker service.

Copyright (c) 2021 Mikhail Medvedev
"""
import logging
from threading import Timer


from website_monitor.config import config
from website_monitor.checker.producer import send_message
from website_monitor.checker.check import check_url


log = logging.getLogger()


def check(url: str, timeout: int, pattern: str = ''):
    """
    Collect mertric and send it over to Kafka
    
    :param url: url to check
    :param timeout: request timeout
    :param pattern: regex pattern to look for on page
    """
    status = check_url(url, timeout=timeout, pattern=pattern)
    send_message(status)


def schedule(url: str, pattern: str):
    """
    Schedule the website availability check to run every config.timeout.

    :param url: url to check
    :param pattern: regex pattern to look for on page
    """
    check(url, config.request_timeout, pattern)
    Timer(config.timeout, schedule, args=(url, pattern)).start()


def run_checker(url: str, pattern: str):
    """
    Start the Checker service.

    :param url: url to check
    :param pattern: regex pattern to look for on page
    """
    log.info('Starting the checker...')
    schedule(url, pattern)
