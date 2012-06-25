@echo off
if "%1"=="full" goto FULL
python .\test\test_driver.py | findstr failed
goto DONE
:FULL

python .\test\test_driver.py
:DONE