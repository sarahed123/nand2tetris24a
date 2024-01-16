# usage: python test_04.py [example]?
#        python -m pytest -xv test_04.py
#        python -m pytest -xv test_04.py::unit_test_func
#        python -m pytest -qrfsp test_04.py
import os
import sys
import subprocess
import pytest

os.chdir(os.path.dirname(os.path.abspath(__file__)))


TOOLS_DIR = '../../tools'
extention = 'bat' if os.name == 'nt' else 'sh'
HWSimulator = os.path.join(os.path.abspath(TOOLS_DIR), f'HardwareSimulator.{extention}')
CPUEmulator = os.path.join(os.path.abspath(TOOLS_DIR), f'CPUEmulator.{extention}')
VMEmulator = os.path.join(os.path.abspath(TOOLS_DIR), f'VMEmulator.{extention}')

chips = ['Mult', 'Fill']

if os.path.exists('runonly.log'):
    with open('runonly.log') as f:
        example = f.readline()
    chips = [chip for chip in chips if chip == example]


@pytest.mark.parametrize("chip", chips)
def test_chip(chip):
    print(f'Testing {chip}.hdl')
    tester_file = chip + 'Automatic' if chip == 'Fill' else chip
    success_msg = b"End of script - Comparison ended successfully" + os.linesep.encode('ascii')
    assert subprocess.check_output([CPUEmulator, f'{chip.lower()}/{tester_file}.tst']) == \
        success_msg, (f'Hardware simulator failure on chip {chip}')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open('runonly.log', 'a') as f:
            f.write(sys.argv[1])
    result = pytest.main(['-x', '-v', __file__])  # -x to stop on first failure, -v verbose output
    if len(sys.argv) > 1:
        os.remove('runonly.log')
    sys.exit(result)
