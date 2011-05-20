#-------------------------------------------------------------------------------
# Name:        tester.py
# Purpose:
#
# Author:      kjells
#
# Created:     19/05/2011
# Copyright:   (c) kjells 2011
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import csv
import sys
from ulp import WithinThisManyULP

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class DataObj(object):
    """ Read a csv file and create a map keyed by lines and columns
        Allow for 2 of these objects to be compared.
    """

    def __init__(self, filename):
        self._filename= filename
        self._map = dict()
        self._cols= []
        self.ReadFile()

    def ReadFile(self):
        reader = csv.DictReader(open(self._filename, 'r'), delimiter=',', quotechar='|')
        self._cols = reader.fieldnames
        for row in reader:
            self._map[row['fuelbed']] = row

    def CompareItems(self, a, b, key, column):
        compare = True
        if isNumber(a) and isNumber(b):
            if not WithinThisManyULP(float(a), float(b), 10000):
                print "{} : {} : {} : {}".format(key, column, a, b)
                compare = False
        return compare

    def Compare(self, other):
        comparisons = 0
        failures = 0
        mykeys = set(self._map.keys())
        otherKeys = set(other._map.keys())
        commonKeys = []
        for key in (mykeys & otherKeys):
            if key.isdigit():
                commonKeys.append(int(key))
        commonKeys = sorted(commonKeys)
        for key in commonKeys:
            key = str(key)
            for col in self._cols:
                if col in other._map[key]:
                    check = self.CompareItems(
                        self._map[key][col], other._map[key][col], key, col)
                    comparisons += 1
                    failures += 1 if not check else 0
        print "\n{} comparisons {} failures".format(comparisons, failures)

def main():
    if len(sys.argv) > 2:
        one = DataObj(sys.argv[1])
        two = DataObj(sys.argv[2])
        one.Compare(two)

if __name__ == '__main__':
    main()
