rem @echo off
if "%1"=="full" goto FULL
set PYTHONPATH=%PYTHONPATH%;%cd%\consume && %py2%\python.exe .\test\test_driver.py | findstr failed
goto DONE
:FULL
set PYTHONPATH=%PYTHONPATH%;%cd%\consume && %py2%\python.exe .\test\test_driver.py
:DONE