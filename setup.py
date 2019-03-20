from setuptools import setup
from consume import version

# Note: using pip.req.parse_requirements like so:
#  > REQUIREMENTS = [str(ir.req) for ir in parse_requirements('requirements.txt')]
# can result in the folloing error (for example, on Heroku):
#    TypeError: parse_requirements() missing 1 required keyword argument: 'session'
with open('requirements.txt') as f:
    REQUIREMENTS = f.read().splitlines()

setup(
    name='apps-consume',
    version='{}.{}.{}'.format(version.MAJOR_VERSION, version.MINOR_VERSION,
        version.PYPI_BUILD_REVISION),
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
