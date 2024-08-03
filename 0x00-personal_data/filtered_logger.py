#!/usr/bin/env python3
"""Personal data
Filtered Logger Module
"""

import re
from typing import List


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str,
) -> str:
    """Get the log message obfuscated"""
    pattern = rf'({"|".join(fields)})=(.*)'
    props = message.split(separator)
    for i in range(len(props)):
        props[i] = re.sub(pattern, rf"\1={redaction}", props[i])
    return separator.join(props)
