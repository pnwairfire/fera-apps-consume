#! /bin/bash
# add '-b' on command line for quiet output
python -m unittest discover  $1 -s  unittest
