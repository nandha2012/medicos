from dataclasses import dataclass
from typing import Optional


@dataclass
class RedcapResponseFirst:
    timestamp: str
    username: str
    action: str
    details: str
    record: str

    def to_dict(self):
        """Convert the dataclass instance to a dictionary."""
        return {
            "timestamp": self.timestamp,
            "username": self.username,
            "action": self.action,
            "details": self.details,
            "record": self.record
        }