#!/usr/bin/env python3

""" Returns the log message obfuscated """

import re


def filter_datum(fields, redaction, message, separator):
    """ Returns the log message obfuscated """
    pattern = r'(' + '|'.join(fields) + r')=.*?' + re.escape(separator)
    return re.sub(pattern, lambda match:
                  match.group(1) + '=' + redaction + separator, message)
