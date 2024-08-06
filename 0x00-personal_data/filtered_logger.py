#!/usr/bin/env python3
"""Personal data
Filtered Logger Module
"""

import logging
import re
from typing import List


PII_FIELDS = ["email", "phone", "ssn", "password", "ip"]


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Redacting Formatter constructor"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Filter the values of  the log record"""
        fmt = super().format(record)
        return filter_datum(self.fields, self.REDACTION, fmt, self.SEPARATOR)


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


def get_logger() -> logging.Logger:
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.WARN)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
