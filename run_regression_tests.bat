@echo off
if "%1"=="full" goto FULL
python .\test\test_driver.py > 00results.txt
type 00results.txt | findstr Exception
type 00results.txt | findstr failed
python consume_batch.py natural test\1_458_english.csv
diff consume_results.csv test\expected\1_458_english_out.csv
python consume_batch.py natural test\1_458_metric.csv
diff consume_results.csv test\expected\1_458_metric_out.csv
goto DONE
:FULL

python .\test\test_driver.py
:DONE