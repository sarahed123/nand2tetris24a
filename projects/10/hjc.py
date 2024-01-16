#!/usr/bin/python32
"""
hjc.py -- Hack computer Jack compiler
Solution provided by Nand2Tetris authors, licensed for educational purposes
Commented and skeleton-ized by Janet Davis, April 18, 2016
Refactored by John Stratton and Janet Davis, April 2019
Adapted to JCE course, 2020-2024a
"""

import sys
import os
from hjcTokens import *
from hjcTokenizer import *
from hjcOutputFile import *


def Process(sourceFileName, outputFileName):
    global source, debug

    if tokens:
        ProcessTokenizerTest(sourceFileName, outputFileName)
        return

    xmlOutputFileName = outputFileName.replace('.vm', '.out.xml')
    print('Processing', sourceFileName, 'to', xmlOutputFileName, ',', outputFileName)

    from hjcCompile import CompileEngine
    compiler = CompileEngine(sourceFileName, outputFileName,
                             xmlOutputFileName, source)
    if debug:
        compiler.CompileClass()
    else:
        try:
            compiler.CompileClass()
        except HjcError as message:
            print(message)
    compiler.Close()


def ProcessTokenizerTest(sourceFileName, outputFileName):
    global source, debug

    outputFileName = outputFileName.replace('.vm', 'T.out.xml')
    print('Processing', sourceFileName, 'to', outputFileName)

    outputFile = OutputFile(outputFileName, 'tokens')

    tokenizer = Tokenizer(sourceFileName, outputFile, source)
    while tokenizer.Advance():
        PrintToken(tokenizer, outputFile)
    outputFile.Close()


def PrintToken(tokenizer, outputFile):
    token = tokenizer.TokenType()
    if token == TK_KEYWORD:
        outputFile.WriteXml('keyword', tokenizer.KeywordStr())
    elif token == TK_SYMBOL:
        outputFile.WriteXml('symbol', tokenizer.Symbol())
    elif token == TK_IDENTIFIER:
        outputFile.WriteXml('identifier', tokenizer.Identifier())
    elif token == TK_INT_CONST:
        outputFile.WriteXml('integerConstant', str(tokenizer.IntVal()))
    elif token == TK_STRING_CONST:
        outputFile.WriteXml('stringConstant', tokenizer.StringVal())
    else:
        raise HjcError('Internal error: bad token type')


def Usage():
    print('usage: hjc [options] sourceFile.jack')
    print('    sourceFile may be a directory in which case all .jack files')
    print('    in the directory will be processed to .vm files')
    print()
    print('    -s option writes source as /// comments in .vm files.')
    sys.exit(-1)


def main():
    global source, debug, tokens
    source = False
    debug = False
    tokens = False
    while True:
        if len(sys.argv) >= 2:
            if sys.argv[1] == '-s':
                source = True
                del (sys.argv[1])
                continue
            if sys.argv[1] == '-d':
                debug = True
                del (sys.argv[1])
                continue
            if sys.argv[1] == '-t':
                tokens = True
                del (sys.argv[1])
                continue
        break

    if len(sys.argv) != 2:
        Usage()

    sourceName = sys.argv[1]

    if os.path.isdir(sourceName):
        # process all .jack files in dir
        dirName = sourceName
        print('Processing directory', dirName)
        for sourceName in os.listdir(dirName):
            if os.path.splitext(sourceName)[1].lower() == os.path.extsep + 'jack':
                outName = os.path.splitext(sourceName)[0] + os.path.extsep + 'vm'
                outName = dirName + os.path.sep + outName
                sourceName = dirName + os.path.sep + sourceName
                Process(sourceName, outName)
    else:
        # process single .jack file
        outName = os.path.splitext(sourceName)[0] + os.path.extsep + 'vm'
        Process(sourceName, outName)


if __name__ == '__main__':
    main()
