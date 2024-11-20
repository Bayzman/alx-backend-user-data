#!/usr/bin/env python3

""" Returns the log message obfuscated """

import re
from typing import List
import logging
import mysql.connector
import os

PII_FIELDS = ("email", "password", "name", "ssn", "phone")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns the log message obfuscated """
    pattern = r'(' + '|'.join(fields) + r')=.*?' + re.escape(separator)
    return re.sub(pattern, lambda match:
                  match.group(1) + '=' + redaction + separator, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filter values in incoming log records using filter_datum """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ Returns a loging.Logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Returns a database connection string """
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    passwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db = os.getenv("PERSONAL_DATA_DB_NAME", "")
    connector = mysql.connector.connect(host=host, user=user,
                                        passwd=passwd, db=db,
                                        port=3306)

    return connector


def main():
    """ Main function """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            message = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, message, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


if __name__ == "__main__":
    main()
