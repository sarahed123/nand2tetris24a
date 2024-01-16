import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from hvmCodeWriter import *
from hvmCommands import *


def test_arithmatic_push_d_returns_fixed_string_comand(temp_output):
    codewriter = CodeWriter(temp_output)  # temp_output is only used here to satisfy the constructor parameter
    asm_code = codewriter._pushD()  # we can debate if testing internals/fix values is encouraged/necessary
    assert '@SP, M=M+1' in asm_code  # only a start, assumes a push operation will include SP++


def test_arithmatic_add_command_is_recognized(temp_output):
    codewriter = CodeWriter(temp_output)  # temp_output is a stub file, that we can "open" and check it's content
    codewriter.writeArithmetic(T_ADD)
    codewriter.close()
    assert '@SP' in temp_output.read_text(encoding="utf-8")  # only a start


@pytest.fixture
def temp_output(tmpdir):
    output = tmpdir.join("output.asm")
    return output
