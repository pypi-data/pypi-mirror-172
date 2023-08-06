# Version needs to change every time it is pushed up to PyPI (Python Package Index)
# version = '1.0.0'
#   - First #: Major Release - changes are incompatible to previous releases
#   - Second #: Minor Release - minor changes such as improving functionality
#   - Third #: patches, bug fixes, very small updates

# install_requires=[...]
#   - if you installed a new pip module when making updates or adding new functionality to this module, please 
#     place it in the brackets

from setuptools import setup
setup(
    name = 'ares-testbed-cli',
    version = '1.0.1',
    packages = ['otbctl'],
    author = 'Venkata Krishna Lolla',
    author_email = 'venkata.lolla@optum.com',
    maintainer = 'Venkata Krishna Lolla',
    url = 'https://github.optum.com/ecp/optum-testbed-cli',
    install_requires=[
        'python-dotenv', 'requests', 'pyyaml', 'tabulate', 'numpy', 'munch', 'validators', 'pygithub', 'schema'
    ],
    scripts=['otbctl_directory.sh'],
    entry_points = {
        'console_scripts': [
            'otbctl = otbctl.__main__:main'
        ]
    }
)
