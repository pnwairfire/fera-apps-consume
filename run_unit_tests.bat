@echo off
set PYTHONPATH=%PYTHONPATH%;%cd%\consume && python -m unittest discover -s unittest