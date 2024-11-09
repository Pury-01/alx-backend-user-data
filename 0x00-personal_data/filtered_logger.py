#!/usr/bin/env python3
"""
function that returns the log message obfuscated.
"""
import re
from typing import List


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
