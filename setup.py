import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='fatzebra',
    use_scm_version={'version_scheme': 'post-release'},
    setup_requires=['setuptools_scm'],
    description='Fat Zebra Python Library',
    long_description=open("README.txt").read(),
    author='Fat Zebra',
    author_email='support@fatzebra.com.au',
    url='https://www.fatzebra.com.au/',
    packages=['fatzebra'],
    install_requires=['requests >= 0.14.2', 'setuptools_scm', 'simplejson'],
    test_suite='test',
)
