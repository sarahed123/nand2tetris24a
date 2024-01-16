@echo off
REM A demo windows batch to migrate from project 07 to project 08
REM Assuming you are on branch main, and you are in terminal on the project folder: cd projects/08
REM run: cmd /c migrate_from_07.cmd, or execute the following commands:

REM Copy source files and previous unit tests 
copy ..\07\hvm*.py
copy ..\07\tests\test_*.py .\tests\

REM Make sure our translator runs here and can produce initial output
python .\hvm.py -d .\ProgramFlow\BasicLoop\
IF EXIST ".\ProgramFlow\BasicLoop\BasicLoop.asm" (
  echo "Good to go"
) ELSE (
  echo "Could not find hvm output"
)

REM add and commit the moved files to the current branch, push it, and then move to project 08 branch

git add .
git commit -m "07 files moved to 08 folder"
git push
git switch -c 08