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
    namespace_packages=['consume'],
    package_data={'consume': ['input_data/*.xml']},
    url=' www.fs.fed.us/pnw/fera',
    license='LICENSE.txt',
    description='Provides a calculator for estimating fuel consumption and emissions as a result of fire.',
    install_requires=['numpy']
    #test_suite='somepackage.tests.get_suite'
)