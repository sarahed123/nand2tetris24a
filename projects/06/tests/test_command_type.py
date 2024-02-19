import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from hasm import *
from hasmUtils import *


def test_command_type_A_command():
    assert command_type("@23") == A_COMMAND, "Should be A_COMMAND"
def test_command_type_L_command():
    assert command_type("(LOOP)") == L_COMMAND, "Should be l_COMMAND"
def test_command_type_C_command():
    assert command_type("M = A") == C_COMMAND, "Should be C_COMMAND"   
def test_command_type_C_command2():
    assert command_type("M = D") == C_COMMAND, "Should be C_COMMAND"   
def test_command_type_A_command2():
    assert command_type("@sarah") == A_COMMAND, "Should be A_COMMAND"


