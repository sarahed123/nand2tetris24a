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
    assert temp_output.read_text()[0] == '(fibonacci)'


@pytest.fixture
def temp_output(tmpdir):
    output = tmpdir.join("output.asm")
    return output
