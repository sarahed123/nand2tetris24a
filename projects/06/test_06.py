# usage: python test_06.py [example]?
#        python -m pytest -xv test_06.py
#        python -m pytest -xv test_06.py::unit_test_func
#        python -m pytest -qrfsp test_06.py
import os
import sys
import subprocess
import pytest
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))


TOOLS_DIR = '../../tools'
extention = 'bat' if os.name == 'nt' else 'sh'
TextComparer = os.path.join(os.path.abspath(TOOLS_DIR), f'TextComparer.{extention}')


@pytest.mark.skipif(os.path.exists('runonly.log'), reason='when having a script parameter')
def test_run_unit_tests():
    '''Testing all unit tests (to install pytest run: pip install -U pytest)'''
    if os.path.exists('runonly.log'):
        pytest.skip()

    def get_collected():
        collected = 0
        coverage_report_file = './pytest-collect.log'
        with open(coverage_report_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if re.search(r'collected', line):
                    collected = int(line.removeprefix('collected').strip().removesuffix('items').removesuffix('item'))
                    break
        return collected

    assert pytest.main(['-x', './tests']) == pytest.ExitCode.OK, 'All unit tests need to pass'
    os.system('python -m pytest --collect-only ./tests > pytest-collect.log')
    required = 4
    assert get_collected() >= required, f'We require at least {required} unit tests.'


dirs = ["add", "max", "rect", "pong"]
# These are some extra small code snippets for tests, not part of the mandatory end2end test
# dirs.extend(["instructions", "symbols"])
if os.path.exists('runonly.log'):
    with open('runonly.log') as f:
        example = f.readline()
    dirs = [dir for dir in dirs if dir == os.path.normpath(example)]

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
programs = []
for dir in dirs:
    for path in os.listdir(os.path.join(dname, dir)):
        filename, extention = os.path.splitext(path)
        if extention == '.asm':
            programs.append(f'{dir}/{filename}')


@pytest.mark.parametrize("program", programs)
def test_program_assembly(program):
    print(f'Testing {program}.asm')
    subprocess.run(f'python hasm.py {program}.asm', shell=True)
    success_msg = b"Comparison ended successfully" + os.linesep.encode('ascii')
    assert subprocess.check_output([TextComparer, f'{program}.hack', f'{program}.cmp']) == \
        success_msg, ('TextComparer failure on program {program}.hack')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open('runonly.log', 'a') as f:
            f.write(sys.argv[1])
    result = pytest.main(['-x', '-v', __file__])  # -x to stop on first failure, -v verbose output
    if len(sys.argv) > 1:
        os.remove('runonly.log')
    sys.exit(result)
