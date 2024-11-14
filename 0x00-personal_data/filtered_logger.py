#!/usr/bin/env python3
"""
function that returns the log message obfuscated.
"""
import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError


def filter_datum(
        fields: str,
        redaction: str,
        message: str,
        separator: str) -> str:
    """obfuscate of specified fields in a log message."""
    pattern = r"(" + "|".join(f"{field}=[^;]*" for field in fields) + ")"
    return re.sub(
            pattern,
            lambda x: f"{x.group().split('=')[0]}={redaction}",
            message
    )
