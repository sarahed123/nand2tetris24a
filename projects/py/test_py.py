# usage: python testpy.py [example]?
#        python -m pytest -xv testpy.py
#        python -m pytest -xv testpy.py::unit_test_func
#        python -m pytest -qrfsp testpy.py
# For running the notebooks with python install jupyter, e.g., pip install jupyter
import os
import sys
import subprocess
import pytest

exercise_dir = './notebooks/beginner/exercises'
exercises = ['strings', 'numbers', 'conditionals', 'lists', 'dictionaries', 'for_loops', 'functions',
             'testing1', 'recap1']

if os.path.exists('runonly.log'):
    with open('runonly.log') as f:
        example = f.readline()
    exercises = [e for e in exercises if e == example]


@pytest.mark.parametrize("exercise", exercises)
def test_notebook(exercise):
    print(f'Testing {exercise}')
    filename = exercise + '_exercise.ipynb'
    subprocess.check_output(
        f'python -m jupyter nbconvert --to notebook --inplace --execute {os.path.join(exercise_dir, filename)}',
        shell=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open('runonly.log', 'a') as f:
            f.write(sys.argv[1])
    result = pytest.main(['-x', '-v', __file__])  # -x to stop on first failure, -v verbose output
    if len(sys.argv) > 1:
        os.remove('runonly.log')
    sys.exit(result)
