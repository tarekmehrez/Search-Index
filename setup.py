"""
Contains the setup script for talata_bont_backend package.
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = dict(

    # meta data
    name='my_search',
    version='1.0',

    # package
    package_dir={'': 'lib'},
    packages=['my_search',
              'my_search.core',
              'my_search.exceptions',
              'my_search.util']
)

setup(**config)
