#-------------------------------------------------------------------------------
# Name:        custom_col.py
# Purpose:
#
# Author:      kjells
#
# Created:     10/10/2011
# Copyright:   (c) kjells 2011
#-------------------------------------------------------------------------------
from xml.etree import ElementTree as ET

from collections import namedtuple
ColumnCfg = namedtuple('ColumnCfg', 'include detail')

def get_element_value(node):
    if None != node:
        text = node.attrib['include'].lower()
        col = True if text == 'yes' or text == 'true' else False
        text = node.attrib['detail'].lower()
        detail = 'total' if text == 'total'  else 'all'
        return ColumnCfg(col, detail)
    else:
        assert False

class CustomCol(object):
    def __init__(self,
        parameters_col = True,
        heat_release_col = ColumnCfg(True, 'all'),
        emissions_col = ColumnCfg(True, 'all'),
        emissions_stratum_col = ColumnCfg(True, 'total'),
        consumption_col = ColumnCfg(True, 'all')
        ):
        self._parameters_col = parameters_col
        self._heat_release_col = heat_release_col
        self._emissions_col = emissions_col
        self._emissions_stratum_col = emissions_stratum_col
        self._consumption_col = consumption_col

    @property
    def parameters_col(self): return self._parameters_col
    @property
    def emissions_col(self): return self._emissions_col
    @property
    def emissions_stratum_col(self): return self._emissions_stratum_col
    @property
    def heat_release_col(self): return self._heat_release_col
    @property
    def consumption_col(self): return self._consumption_col

    @classmethod
    def from_file(cls, filename):
        ''' Approximate second constructor, for use with a file.
        '''
        tree =  ET.parse(filename)
        root = tree.getroot()
        node = root.find('parameters_column')
        text = node.attrib['include'].lower()
        p_col = True if text == 'yes' or text == 'true' else False
        hr_col = get_element_value(root.find('heat_release_column'))
        em_node = root.find('emissions_column')
        em_col = get_element_value(em_node)
        em_st_col = get_element_value(em_node.find('stratum_column'))
        cons_col = get_element_value(root.find('consumption_column'))
        return cls( parameters_col=p_col,
                    heat_release_col=hr_col,
                    emissions_col=em_col,
                    emissions_stratum_col=em_st_col,
                    consumption_col=cons_col)


def main():
    c = CustomCol.from_file("custom.xml")
    print(c.parameters_col)
    print(c.emissions_col)
    print(c.emissions_stratum_col)
    print(c.heat_release_col)
    print(c.consumption_col)
    d = CustomCol()
    print(d.parameters_col)
    print(d.emissions_col)
    print(d.emissions_stratum_col)
    print(d.heat_release_col)
    print(d.consumption_col)

if __name__ == '__main__':
    main()