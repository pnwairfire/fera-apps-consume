#-------------------------------------------------------------------------------
# Name:        cmdline.py
# Purpose:
#
# Author:      kjells
#
# Created:     12/10/2011
# Copyright:   (c) kjells 2011
#-------------------------------------------------------------------------------
import sys
import os
import argparse

def print_default_column_config_xml(filename):
    DEFAULT_XML = r'''
<consume_output>
    <!-- Include the parameters data? yes/no. How much detail? all/total. -->
    <parameters_column include="yes" />

    <!-- Include the heat release data? yes/no. How much detail? all/total. -->
    <heat_release_column include="no" detail="all" />

    <!-- Include the emissions data? yes/no. How much detail? all/total. -->
    <emissions_column include="no" detail="all">
        <stratum_column  include="no" detail="total"  />
    </emissions_column>

    <!-- Include the consumption data? yes/no. How much detail? all/total. -->
    <consumption_column include="yes" detail="total"  />
</consume_output>
    '''
    with open(filename, 'w') as outfile:
        for line in DEFAULT_XML:
            outfile.write(line)

def make_parser():
    parser = argparse.ArgumentParser(
        description="Generate consumption, emissions, and heat release data."
    )
    parser.add_argument('-c', '--csv', action='store', nargs=1, dest='csv_file',
        help='Specify the csv input file for consume to use')
    parser.add_argument('-x', '--xml_column_cfg', action='store', nargs=1, dest='col_cfg_file',
        help='Specify the output column configuration file for consume to use')
    parser.add_argument('-g', '--generate_column_config', action='store', nargs='?',
        default="", const="output_config.xml", dest='gen_col_cfg',
        help='This option will print a default column configuration xml file to the console. \
            Redirect to a file and customize to suit your needs.\
            %(prog)s --generate_column_config > my_config.xml\n'
        )
    return parser

class ConsumeParser(object):
    def __init__(self, argv):
        parser = make_parser()
        if 1 == len(argv):
            parser.parse_args(['--help'])
        else:
            args = parser.parse_args(argv[1:])
            if args.gen_col_cfg:
                print_default_column_config_xml(args.gen_col_cfg)
                exit(0)
            if self.exists(args.csv_file[0]):
                self._csv_file = args.csv_file[0]
            if self.exists(args.col_cfg_file[0]):
                self._col_cfg_file = args.col_cfg_file[0]

    def exists(self, filename):
        if not os.path.exists(filename):
            print("Error: file not found \"{}\"".format(filename))
            exit(1)
        return True

    @property
    def csv_file(self): return self._csv_file
    @property
    def col_cfg_file(self): return self._col_cfg_file


def main():
    ConsumeParser(sys.argv)

if __name__ == '__main__':
    main()
