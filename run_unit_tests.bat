@echo off
set PYTHONPATH=%PYTHONPATH%;%cd%\consume && python -m unittest discover -s -q -b .
set PYTHONPATH=%PYTHONPATH%;%cd%\consume && python -m unittest discover -s -q -b unittest