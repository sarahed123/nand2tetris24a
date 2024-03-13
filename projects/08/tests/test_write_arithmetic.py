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

def test_arithmatic_pop_d_returns_fixed_string_comand(temp_output):
    codewriter = CodeWriter(temp_output)  # temp_output is only used here to satisfy the constructor parameter
    asm_code = codewriter._popD()  # we can debate if testing internals/fix values is encouraged/necessary
    assert '@SP, M=M-1' in asm_code  # only a start, assumes a pop operation will include SP--

def test_write_push_pop_returns_fixed_string_comand(temp_output):
    codewriter = CodeWriter(temp_output)  # temp_output is only used here to satisfy the constructor parameter
    codewriter.writePushPop(C_PUSH,'constant',3)  # we can debate if testing internals/fix values is encouraged/necessary
    codewriter.close()
    assert 'D=A' in temp_output.read_text(encoding="utf-8")

def test_arithmatic_gt_command_is_recognized(temp_output):
    codewriter = CodeWriter(temp_output)  # temp_output is a stub file, that we can "open" and check it's content
    codewriter.writeArithmetic(T_GT)
    codewriter.close()
    assert 'D=M-D' in temp_output.read_text(encoding="utf-8")  # only a start

def test_arithmatic_add_command_is_recognized(temp_output):
    codewriter = CodeWriter(temp_output)  # temp_output is a stub file, that we can "open" and check it's content
    codewriter.writeArithmetic(T_ADD)
    codewriter.close()
    assert '@SP' in temp_output.read_text(encoding="utf-8")  # only a start


def test_write_push_pop_returns_fixed_string_comand2(temp_output):
    codewriter = CodeWriter(temp_output)  # temp_output is only used here to satisfy the constructor parameter
    codewriter.writePushPop(C_POP,'this',3)  # we can debate if testing internals/fix values is encouraged/necessary
    codewriter.close()
    assert '@R13' in temp_output.read_text(encoding="utf-8") 


    


@pytest.fixture
def temp_output(tmpdir):
    output = tmpdir.join("output.asm")
    return output
