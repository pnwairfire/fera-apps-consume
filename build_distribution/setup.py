try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

setup(
    name='consume',
    version='4.1',
    author='Michigan Tech Research, Fire and Environmental Research Applications Team (FERA)',
    #author_email='',
    packages=['consume'],
    url=' www.fs.fed.us/pnw/fera',
    license='LICENSE.txt',
    description='Provides a calculator for estimating fuel consumption and emissions as a result of fire.',
    #test_suite='somepackage.tests.get_suite'
)