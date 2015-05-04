@echo off
if "%1"=="full" goto FULL
c:\FuelFireTools_Apr27\bin\python -m test.test_driver > 00results.txt
type 00results.txt | findstr Exception
type 00results.txt | findstr failed
rem python consume_batch.py natural test\1_458_english.csv
rem diff consume_results.csv test\expected\1_458_english_out.csv
rem python consume_batch.py natural test\1_458_metric.csv
rem diff consume_results.csv test\expected\1_458_metric_out.csv
goto DONE
:FULL
c:\FuelFireTools_Apr27\bin\python -m test.test_driver 
:DONE