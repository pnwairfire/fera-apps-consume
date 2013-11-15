@echo off
if "%1"=="full" goto FULL
python .\test\test_driver.py > 00results.txt
type 00results.txt | findstr Exception
type 00results.txt | findstr failedgoto DONE
:FULL

python .\test\test_driver.py
:DONE