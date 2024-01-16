# usage: python test10.py [example]?
#        python -m pytest -xv test_10.py
#        python -m pytest -xv test_10.py::unit_test_func
#        python -m pytest -qrfsp test_10.py
import os
import sys
import subprocess
import pytest

os.chdir(os.path.dirname(os.path.abspath(__file__)))


TOOLS_DIR = '../../tools'
extention = 'bat' if os.name == 'nt' else 'sh'
CPUEmulator = os.path.join(os.path.abspath(TOOLS_DIR), f'CPUEmulator.{extention}')
VMEmulator = os.path.join(os.path.abspath(TOOLS_DIR), f'VMEmulator.{extention}')
TextComparer = os.path.join(os.path.abspath(TOOLS_DIR), f'TextComparer.{extention}')

programs = ["ExpressionLessSquare", "Square", "ArrayTest"]

if os.path.exists('runonly.log'):
    with open('runonly.log') as f:
        example = f.readline()
    programs = [p for p in programs if p == os.path.normpath(example)]


@pytest.mark.parametrize("program", programs)
def test_program_tokenizing(program):
    success_msg = b"Comparison ended successfully" + os.linesep.encode('ascii')
    subprocess.run(f'python hjc.py -t {program}', shell=True)
    for path in os.listdir(program):
        filename, extention = os.path.splitext(path)
        if extention == '.jack':
            print(f'Testing {program}/{filename}')
            assert subprocess.check_output([TextComparer, f'{program}/{filename}T.out.xml',
                                           f'{program}/{filename}T.xml']) == \
                success_msg, (f'TextComparer failure on {program}/{filename}')


@pytest.mark.parametrize("program", programs)
def test_program_parsing(program):
    success_msg = b"Comparison ended successfully" + os.linesep.encode('ascii')
    subprocess.run(f'python hjc.py {program}', shell=True)
    for path in os.listdir(program):
        filename, extention = os.path.splitext(path)
        if extention == '.jack':
            print(f'Testing {program}/{filename}')
            assert subprocess.check_output([TextComparer, f'{program}/{filename}.out.xml',
                   f'{program}/{filename}.xml']) == success_msg, (f'TextComparer failure on {program}/{filename}')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open('runonly.log', 'a') as f:
            f.write(sys.argv[1])
    result = pytest.main(['-x', '-v', __file__])  # -x to stop on first failure, -v verbose output
    if len(sys.argv) > 1:
        os.remove('runonly.log')
    sys.exit(result)
