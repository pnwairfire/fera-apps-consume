@echo off
if "%1"=="full" goto FULL
set PYTHONPATH=%PYTHONPATH%;%cd%\consume && c:\progfiles_x86\Python27\python.exe .\test\test_driver.py | findstr failed
goto DONE
:FULL
set PYTHONPATH=%PYTHONPATH%;%cd%\consume && c:\progfiles_x86\Python27\python.exe .\test\test_driver.py
:DONE