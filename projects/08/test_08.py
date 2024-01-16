# usage: python test_08.py [example]?
#        python -m pytest -xv test_08.py
#        python -m pytest -xv test_08.py::unit_test_func
#        python -m pytest -qrfsp test_08.py
import os
import sys
import subprocess
import pytest
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))


TOOLS_DIR = '../../tools'
extention = 'bat' if os.name == 'nt' else 'sh'
CPUEmulator = os.path.join(os.path.abspath(TOOLS_DIR), f'CPUEmulator.{extention}')
VMEmulator = os.path.join(os.path.abspath(TOOLS_DIR), f'VMEmulator.{extention}')


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
    required = 10
    assert get_collected() >= required, f'We require at least {required} unit tests (you can carry over from previous \
        project, and add at least {required/2}.'


@pytest.mark.skipif(os.path.exists('runonly.log'), reason='when having a script parameter')
def test_run_unit_tests_with_coverage():
    '''Running coverage and producing xml report (to install pytest-cov run: pip install -U pytest-cov)'''
    if os.path.exists('runonly.log'):
        pytest.skip()

    def get_coverage():
        precentage = -1
        coverage_report_file = './coverage.log'
        with open(coverage_report_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if re.search(r'TOTAL', line):
                    precentage = int(line.removeprefix('TOTAL').strip().removesuffix('%').split(' ')[-1])
                    break
        return precentage

    os.system('python -m pytest ./tests/ --cov=hvmCodeWriter --cov-report term --cov-report html')
    os.system('python -m pytest ./tests/ --cov=hvmCodeWriter --cov-report term  > coverage.log')
    
    required = 85
    precentage = get_coverage()
    assert precentage != -1, 'Falied to read coverage report: coverage.log'
    assert precentage >= required, f'We require a coverage of at least {required}%.'


programs = ['ProgramFlow/BasicLoop', 'ProgramFlow/FibonacciSeries',
            'FunctionCalls/SimpleFunction', 'FunctionCalls/NestedCall', 'FunctionCalls/FibonacciElement',
            'FunctionCalls/StaticsTest']

if os.path.exists('runonly.log'):
    with open('runonly.log') as f:
        example = f.readline()
    programs = [p for p in programs if os.path.normpath(p) == os.path.normpath(example)]


@pytest.mark.parametrize("program", programs)
def test_program_compilation(program):
    print(f'Testing {program}')
    sys_file = os.path.join(program, "Sys.vm")
    init_flag = "" if os.path.exists(sys_file) else "-n"
    success_msg = b"End of script - Comparison ended successfully" + os.linesep.encode('ascii')
    subprocess.run(f'python hvm.py {init_flag} -d {program}', shell=True)
    assert subprocess.check_output([CPUEmulator, f'{program}/{program.split("/")[1]}.tst']) == \
        success_msg, (f'CPU emulator failure on program {program}')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open('runonly.log', 'a') as f:
            f.write(sys.argv[1])
    result = pytest.main(['-x', '-v', __file__])  # -x to stop on first failure, -v verbose output
    if len(sys.argv) > 1:
        os.remove('runonly.log')
    sys.exit(result)
