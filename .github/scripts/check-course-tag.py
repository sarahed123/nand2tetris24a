#!/bin/python3
import sys
import os

project = sys.argv[1]
tag = '2024a'

file_for_tag = {'00': 'Xor.hdl',
                '01': 'Xor.hdl',
                '04': 'mult/Mult.asm',
                'py': 'notebooks/beginner/exercises/strings_exercise.ipynb',
                '06': 'hasm.py',
                '07': 'hvm.py',
                '08': 'hvm.py',
                '09': 'Square/Main.jack',
                '10': 'hjc.py',
                '11': 'hjc.py'
                }

result = 0
file = file_for_tag.get(project, f'test_{project}.py')
path = f'./projects/{project}/{file}'
if not os.path.exists(path):
    result = 1
else:
    with open(path, 'r') as f:
        file_content = f.read()
        if tag not in file_content:
            result = 2

print(result)
