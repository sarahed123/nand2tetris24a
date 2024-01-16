@echo off
REM A demo windows batch to migrate from project 10 to project 11
REM Assuming you are on branch main, and you are in terminal on the project folder: cd projects/11
REM run: cmd /c migrate_from_10.cmd, or execute the following commands:


REM Copy source files and possibly system tests for checking the SymbolTable
copy ..\10\hjc*.py
REM copy ..\10\ExpressionLessSquare\*.jack .

REM Make sure our compiler runs here and can produce initial output
python .\hjc.py -d .\Seven\
IF EXIST ".\Seven\Main.vm" (
  echo "Good to go"
) ELSE (
  echo "Could not find hjc output"
)

REM add and commit the moved files to the current branch, push it, and then move to project 11 branch

git add .
git commit -m "10 files moved to 11 folder"
git push
git switch -c 11