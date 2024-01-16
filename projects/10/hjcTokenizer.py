"""
hvmParser.py -- Tokenizer class for Hack Jack compiler
Solution provided by Nand2Tetris authors, licensed for educational purposes
Commented, refactored, and skeleton-ized by Janet Davis, April 18, 2016
Refactored by John Stratton and Janet Davis, April 2019
Adapted to JCE course, 2020-2024a
"""

import string
from hjcTokens import *
from hjcError import *

symbols = '{}()[].,;+-*/&|<>=~'
numberChars = string.digits
numberStart = numberChars
identifierStart = string.ascii_letters + '_'
identifierChars = identifierStart + numberChars
keywords = {
    'boolean' : KW_BOOLEAN,
    'char' : KW_CHAR,
    'class' : KW_CLASS,
    'constructor' : KW_CONSTRUCTOR,
    'do' : KW_DO,
    'else' : KW_ELSE,
    'false' : KW_FALSE,
    'field' : KW_FIELD,
    'function' : KW_FUNCTION,
    'if' : KW_IF,
    'int' : KW_INT,
    'let' : KW_LET,
    'method' : KW_METHOD,
    'null' : KW_NULL,
    'return' : KW_RETURN,
    'static' : KW_STATIC,
    'this' : KW_THIS,
    'true' : KW_TRUE,
    'var' : KW_VAR,
    'void' : KW_VOID,
    'while' : KW_WHILE
}


class Tokenizer(object):
    def __init__(self, sourceName, outputFile=None, source=False):
        """
        Opens 'sourceFile' and gets ready to parse it.
        """
        self.file = open(sourceName, 'r')
        self.lineNumber = 0
        self.line = ''
        self.rawline = ''
        self.inComment = False
        self.printSource = source
        self.outputFile = outputFile

    def Advance(self):
        """
        Reads the next command from the input and makes it the current
        command.
        Returns True if a command was found, False at end of file.
        """
        # Indefine loop; keep reading until we read something other than
        # whitespace and comments
        while True:
            if len(self.line) == 0:
                if not self.file:
                    # File closed; no more tokens
                    return False

                else:
                    # Read next line
                    self.rawline = self.file.readline()
                    if len(self.rawline) == 0:
                        return False  # End of file
                    self.lineNumber = self.lineNumber + 1

                    # Remove ending line break, preserving other white space
                    self.rawline = self.rawline.replace('\n', '')
                    self.line = self.rawline

                    # Print source line as a comment in the output file
                    if (self.printSource):
                        self.outputFile.WriteXml('source',
                                                 '/// %d: %s' % (self.lineNumber, self.rawline))

                    # Skip over comments in the source file
                    self._SkipComments()

                    # Replace tabs with spaces and strip leading/trailing white space
                    self.line = self.line.replace('\t', ' ').strip()

                    # If nothing is left, read another line
                    if len(self.line) == 0:
                        continue

            # Attempt to parse a token from the current line
            self._Parse()

            # If no token was found, read the next line and try again
            if self.token == (None, None):
                continue

            # When a token is finally found, return true!
            return True

    def LineNumber(self):
        return self.lineNumber

    def LineStr(self):
        return self.rawline

    def TokenType(self):
        return self.token[0]

    def TokenTypeStr(self):
        """
        Returns a string representing the token type.
        """
        if self.token[0] == TK_SYMBOL or self.token[0] == TK_KEYWORD:
            return '"' + self.token[1] + '"'
        return tokenTypes[self.token[0]]

    def Keyword(self):
        """
        Returns the current token if it is a keyword.
        Otherwise, raises an error.
        """
        if (self.token[0] == TK_KEYWORD):
            return keywords[self.token[1]]
        raise HjcError('Request for keyword when current token is ' + tokenTypes[self.token[0]])

    def KeywordStr(self, keywordId=None):
        """
        Returns a string representation of the given numeric token ID,
        or the current token if it is a keyword.
        """
        if (keywordId is not None):
            for k in keywords:
                if keywords[k] == keywordId:
                    return k
            raise ValueError
        if (self.token[0] == TK_KEYWORD):
            return self.token[1]

    def Symbol(self):
        """
        Returns the current token if it is a symbol.
        Otherwise, raises an error.
        """
        if (self.token[0] == TK_SYMBOL):
            return self.token[1]
        raise HjcError('Request for symbol when current token is ' + tokenTypes[self.token[0]])

    def Identifier(self):
        """
        Returns the current token if it is an identifier.
        Otherwise, raises an error.
        """
        if (self.token[0] == TK_IDENTIFIER):
            return self.token[1]
        raise HjcError('Request for identifier when current token is ' + tokenTypes[self.token[0]])

    def IntVal(self):
        """
        Returns the integer value of the current token, if it is an integer constant.
        Otherwise, raises an error.
        """
        if (self.token[0] == TK_INT_CONST):
            return int(self.token[1])
        raise HjcError('Request for integer constant when current token is ' + tokenTypes[self.token[0]])

    def StringVal(self):
        """
        Returns the current token if it is a string constant.
        Otherwise, raises an error.
        """
        if (self.token[0] == TK_STRING_CONST):
            return self.token[1]
        raise HjcError('Request for string literal when current token is ' + tokenTypes[self.token[0]])

    def _SkipComments(self):
        """
        If there are comments next in the input stream, skips over them
        to the next token.
        """
        # Look for // comments and remove them
        i = self.line.find('//')
        if i != -1:
            self.line = self.line[:i]

        # If in a multiline comment, see if we have reached the end
        if self.inComment:
            i = self.line.find('*/')
            if i == -1:
                # still in multiline comment
                self.line = ''
            else:
                # end of multiline comment
                self.line = self.line[i + 2:]
                self.inComment = False

        # Look for the start of a /* */ comment
        i = self.line.find('/*')
        while i != -1:
            j = self.line.find('*/')
            if j != -1:
                # inline comment
                self.line = self.line[:i] + ' ' + self.line[j + 2:]
            else:
                # start of multiline comment
                self.line = self.line[:i]
                self.inComment = True
                break
            # There might be another inline comment
            i = self.line.find('/*')

    def _Parse(self):
        """
        Parses the next token, storing it in self.token.
        """
        self.token = (None, None)
        # self.token is a tuple whose first element should be the token type,
        #    and whose second item is the character(s) making up the token.

        while len(self.line):     # Characters remain
            ch = self.line[0]     # Get the next charater
            if ch == ' ':         # Skip spaces; they are not represented in the parse tree
                self.line = self.line[1:]
                continue
            if ch in symbols:     # Parse a symbol
                self.line = self.line[1:]
                self.token = (TK_SYMBOL, ch)
                return
            # TODO-10T-1: Identify whether the current character begins an
            #    integer constant, string constant, or identifier/keyword, and
            #    call the appropriate _Parse helper below.
            #    In each case, set self.token to store the parsed token.
            # HINT: See constants defined at the top of this file: keywords, symbols, identifierStart, identifierChars, etc.
            #       See local Parse methods below
            raise HjcError('Syntax error in line ' + str(self.lineNumber) + ': illegal character "' + ch + '"')

    def _ParseIdentifier(self):
        """
        Parse and return a string representing an identifier or keyword.
        """
        # TODO-10T-2: Compute the return value
        self.line = self.line[1:]
        return ""

    def _ParseInt(self):
        """
        Parses and returns a non-negative integer (converted to int type)
        """
        # TODO-10T-3: Compute the return value
        self.line = self.line[1:]
        return 0

    def _ParseString(self):
        """
        Parses and returns a string constant, NOT INCLUDING the quotes.
        Throws an error if the line ends without a closing quotation mark.
        """
        # TODO-10T-4: Compute the return value
        self.line = self.line[1:]
        raise HjcError('Syntax error in line ' + str(self.lineNumber) + ': open string constant')
