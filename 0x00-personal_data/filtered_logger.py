#!/usr/bin/env python3
"""Personal data
Filtered Logger Module
"""

import logging
import re
from typing import Iterable


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Iterable[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Filter the values of  the log record"""
        print(record)
        return filter_datum(self.fields, self.REDACTION, record, self.SEPARATOR)


def filter_datum(
    fields: Iterable[str],
    redaction: str,
    message: str,
    separator: str,
) -> str:
    """Get the log message obfuscated"""
    pattern = rf'({"|".join(fields)})(.)(.*)'
    props = message.split(separator)
    for i in range(len(props)):
        props[i] = re.sub(pattern, rf"\1\2{redaction}", props[i])
    return separator.join(props)


message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
log_record = logging.LogRecord("my_logger", logging.INFO, None, None, message, None, None)
formatter = RedactingFormatter(fields=("email", "ssn", "password"))
print(formatter.format(log_record))
