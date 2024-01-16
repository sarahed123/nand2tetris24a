# usage: python test_09.py
#        python -m pytest -xv test_09.py
#        python -m pytest -xv test_09.py::unit_test_func
#        python -m pytest -qrfsp test_09.py
import os
import sys
import subprocess
import pytest

os.chdir(os.path.dirname(os.path.abspath(__file__)))

TOOLS_DIR = '../../tools'
extention = 'bat' if os.name == 'nt' else 'sh'
JackCompiler = os.path.join(os.path.abspath(TOOLS_DIR), f'JackCompiler.{extention}')

def extract_last_word(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline()
        last_word = first_line.split()[-1]
        return last_word


def count_files_with_suffix(folder_name, file_suffix):
    count = 0

    # Check if the folder exists
    if not os.path.exists(folder_name):
        print(f"Folder '{folder_name}' does not exist.")
        return count

    # Iterate over all files in the folder
    for file_name in os.listdir(folder_name):
        if file_name.endswith(file_suffix):
            count += 1

    return count

    
def test_jack_program_has_three_compiled_files():
    '''check that there is a manual instruction file, like the test_example.md
       or better script the JackCompiler & VMEmulator to load and check you program automatically'''
    test_filename = "test.md"
    appName = extract_last_word(test_filename)

    subprocess.run(f'{JackCompiler} {appName}', shell=True)

    assert count_files_with_suffix(appName, 'vm') >= 3, f'missing vm files in {appName} folder'


if __name__ == "__main__":
    result = pytest.main(['-x', '-v', __file__])  # -x to stop on first failure, -v verbose output
    sys.exit(result)
