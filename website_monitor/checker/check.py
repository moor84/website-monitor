"""
Website availability checker utils.

Copyright (c) 2021 Mikhail Medvedev
"""
import re
from datetime import datetime, timezone

import requests

from website_monitor.status import Status


def check_url(url: str, timeout: int = 10, pattern: str = '') -> Status:
    """
    Check website for availability.

    :param url: url to check
    :param timeout: request timeout
    :param pattern: regex pattern to look for on page
    :return: Status instance
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    resp = requests.get(url, timeout=timeout)

    regex_check = False
    if pattern and resp.ok:
        if re.search(pattern, resp.text):
            regex_check = True

    return Status(url, timestamp, resp.status_code, resp.elapsed.total_seconds(), regex_check)
