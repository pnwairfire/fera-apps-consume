#/home/kjells/opt/mypy2/bin/python -m test.test_driver > 00results.txt
python -m test.test_driver > 00results.txt
grep -i exception 00results.txt
grep -i failed 00results.txt
