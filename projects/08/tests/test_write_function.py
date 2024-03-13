import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from hvmCodeWriter import *  # need to bring sources from project 07
from hvmCommands import *


def test_write_function(temp_output):
    codewriter = CodeWriter(temp_output)
    codewriter.writeFunction('fibonacci', 1)
    codewriter.close()
    # this is only a start
    assert temp_output.read_text(encoding='utf-8').split('\n')[1] == '(fibonacci)'

def test_write_function2(temp_output):
    codewriter = CodeWriter(temp_output)
    codewriter.writeFunction('test', 2)
    codewriter.close()
    # print("file!: ",temp_output)
    # this is only a start
    assert temp_output.read_text(encoding='utf-8').split('\n')[1] == '(test)'


def test_write_return(temp_output):
    codewriter = CodeWriter(temp_output)
    codewriter.writeReturn()
    codewriter.close()
    # this is only a start
    assert temp_output.read_text(encoding='utf-8').split('\n')[1] == '@LCL'

def test_write_init(temp_output):
    codewriter = CodeWriter(temp_output)
    codewriter.writeInit()
    codewriter.close()
    # this is only a start
    assert temp_output.read_text(encoding='utf-8').split('\n')[2] == 'D=A'

                
def test_write_label(temp_output):
    codewriter = CodeWriter(temp_output)
    codewriter.writeLabel("label_1")
    codewriter.close()
    # this is only a start
    assert temp_output.read_text(encoding='utf-8').split('\n')[1] == '(label_1)'

def test_write_goto(temp_output):
    codewriter = CodeWriter(temp_output)
    codewriter.writeGoto("label_1")
    codewriter.close()
    # this is only a start
    assert temp_output.read_text(encoding='utf-8').split('\n')[2] == '0;JMP'

def test_write_if(temp_output):
    codewriter = CodeWriter(temp_output)
    codewriter.writeIf("label_1")
    codewriter.close()
    # this is only a start
    assert temp_output.read_text(encoding='utf-8').split('\n')[1] == '@SP'

def test_write_call(temp_output):
    codewriter = CodeWriter(temp_output)
    codewriter.writeCall('test', 2)
    codewriter.close()
    # this is only a start
    assert temp_output.read_text(encoding='utf-8').split('\n')[2] == 'D=A'


@pytest.fixture
def temp_output(tmpdir):
    output = tmpdir.join("output.asm")
    return output
