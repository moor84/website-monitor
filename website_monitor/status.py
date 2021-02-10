"""
Metrics dataclass.

Copyright (c) 2021 Mikhail Medvedev
"""
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Status:
    """Website availability metric"""
    url: str
    timestamp: str
    status_code: int
    response_time: float
    regex_check: bool
    
    @property
    def parsed_timestamp(self):
        """This will attempt to parse the timestamp"""
        return datetime.fromisoformat(self.timestamp).astimezone(timezone.utc)
