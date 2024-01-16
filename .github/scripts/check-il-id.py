#!/bin/python3
import sys

input = sys.argv[1] if len(sys.argv) > 1 else ""
sID = input.strip()

if len(sID) == 0:  # empty id is not OK with us (will fail outside for the first)
    result = -1
elif len(sID) != 9:
    result = 1
else:
    IdList = list()
    try:
        id = list(map(int, sID))
        counter = 0

        for i in range(9):
            id[i] *= (i % 2) + 1
            if (id[i] > 9):
                id[i] -= 9
            counter += id[i]

        if (counter % 10 == 0):
            result = 0
        else:
            result = 1
    except:
        result = 1

print(result)
