# usage: python test11.py [example]?
#        python -m pytest -xv test_11.py
#        python -m pytest -xv test_11.py::unit_test_func
#        python -m pytest -qrfsp test_11.py
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

# if you want to first test the SymbolTable implementation,
# you might want to also bring the project's 10 examples over here

programs = ["Seven", "ConvertToBin", "Square", "Average", "Pong", "ComplexArrays"]

if os.path.exists('runonly.log'):
    with open('runonly.log') as f:
        example = f.readline()
    programs = [p for p in programs if p == os.path.normpath(example)]


@pytest.mark.parametrize("program", programs)
def test_program_compilation(program):
    print(f'Testing {program}.')
    # delete all vm files in folder "program"
    for path in os.listdir(program):  # os.listdir() returns a list of all files and folders in a directory
        filename, extention = os.path.splitext(path)
        if extention == '.vm':
            os.remove(f'{program}/{filename}.vm')
    
    # run the compiler and chck that vm files were created
    subprocess.run(f'python hjc.py {program}', shell=True)
    for path in os.listdir(program):
        filename, extention = os.path.splitext(path)
        if extention == '.jack':
            assert os.path.isfile(f'{program}/{filename}.vm') and \
                os.stat(f'{program}/{filename}.vm').st_size > 0, f'Missing or empty {filename}.vm file'
    print('Also test program manually with VMEmulator!')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open('runonly.log', 'a') as f:
            f.write(sys.argv[1])
    result = pytest.main(['-x', '-v', __file__])  # -x to stop on first failure, -v verbose output
    if len(sys.argv) > 1:
        os.remove('runonly.log')
    sys.exit(result)
