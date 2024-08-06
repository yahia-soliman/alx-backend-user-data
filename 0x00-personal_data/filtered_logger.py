#!/usr/bin/env python3
"""Personal data
Filtered Logger Module
"""

import logging
import re
from os import getenv
from typing import List

from mysql.connector.connection import MySQLConnection

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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
    """Create a new logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> MySQLConnection:
    """Get MySQL database connection"""
    host = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    user = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    pwd = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db = getenv("PERSONAL_DATA_DB_NAME")
    return MySQLConnection(user=user, password=pwd, host=host, database=db)


def main():
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT name, email, phone, ssn, password"
        ", ip, last_login, user_agent FROM users;"
    )
    msg = (
        "name={}; email={}; phone={}; ssn={}; password={};"
        " ip={}; last_login={} user_agent={}"
    )
    for row in cursor:
        logger.info(msg.format(*row))
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
