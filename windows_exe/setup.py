try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup
import py2exe

consume_data_files = [
    ('./consume/input_data', ['./consume/input_data/EmissionsFactorDatabase.xml']),
    ('./consume/input_data', ['./consume/input_data/fccs_loadings_1_458.xml']),
]

setup(
    name='consume_batch',
    version='1.0',
    author='Fire and Environmental Research Applications Team (FERA), Michigan Tech Research',
    url=' www.fs.fed.us/pnw/fera',
    license='LICENSE.txt',
    description='Provides a calculator for estimating fuel consumption and emissions as a result of fire.',
    install_requires=['numpy'],
    console=['consume_batch.py'],
    data_files=consume_data_files
    #test_suite='somepackage.tests.get_suite'
)