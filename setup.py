# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyhwschema',
    version='0.0.1',
    description='Python API for Hortonworks Schema Registry',
    long_description=readme,
    author='Ken Tore Tallakstad',
    author_email='tallakstad@gmail.com',
    url='https://github.com/kentore82/pyhwschema',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

