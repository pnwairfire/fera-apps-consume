import os
from setuptools import setup

# Note: using pip.req.parse_requirements like so:
#  > REQUIREMENTS = [str(ir.req) for ir in parse_requirements('requirements.txt')]
# can result in the folloing error (for example, on Heroku):
#    TypeError: parse_requirements() missing 1 required keyword argument: 'session'
with open('requirements.txt') as f:
    REQUIREMENTS = f.read().splitlines()

# HACK: we can't import consume.version because there's no guarantee that
#   any of the dependencies indirectly imported by consume.__init__.py
#   (numpy, pandas, etc.) have yet been installed.  So, parse the file
#   for the version numbers.
version = {}
with open('consume/version.py') as f:
    for line in f.readlines():
        line = line.strip()
        if not line.startswith('#'):
            parts = [p.strip() for p in line.split('=')]
            if len(parts) == 2:
                version[parts[0]] = parts[1]

setup(
    name='apps-consume',
    version='{}.{}.{}'.format(
        version['MAJOR_VERSION'],
        version['MINOR_VERSION'],
        version['PYPI_BUILD_REVISION']
    ),
    author='Fire and Environmental Research Applications Team (FERA)',
    #author_email='',
    packages=[
        'consume'
    ],
    package_data={
        'consume': [
            'input_data/*.xml',
            'input_data/*.csv'
        ]
    },
    scripts=[],
    url='ssh://hg@bitbucket.org/fera/apps-consume4',
    description='Calculates estimated fuel consumption by wild fires.',
    install_requires=REQUIREMENTS,
)
