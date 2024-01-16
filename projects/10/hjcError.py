"""
hjcError.py -- Error exceptions for Hack Jack compiler
Solution provided by Nand2Tetris authors, licensed for educational purposes
"""

import sys


class HjcError(Exception):
    pass


def Error(message, lineNumber=0, line=''):
    """
    Print an error message and continue.
    """
    if lineNumber != 0:
        print('Line %d: %s' % (lineNumber, line))
        print('     ' + message)
    else:
        print(message)
    print('')


def FatalError(message, lineNumber=0, line=''):
    """
    Print an error message and abort.
    """
    Error(message, lineNumber, line)
    sys.exit(-1)

