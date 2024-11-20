#!/usr/bin/env python3

""" Returns the log message obfuscated """

import re
from typing import List


def filter_datum(fields: List[str | int], redaction: List[str | int],
                 message: List[str], separator: str) -> str:
    """ Returns the log message obfuscated """
    pattern = r'(' + '|'.join(fields) + r')=.*?' + re.escape(separator)
    return re.sub(pattern, lambda match:
                  match.group(1) + '=' + redaction + separator, message)
