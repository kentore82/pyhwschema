# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyhwschema',
    version='0.0.2',
    install_requires=requirements,
    description='Python API for Hortonworks Schema Registry',
    long_description='Python API for Hortonworks Schema Registry',
    long_description_content_type='text/markdown',
    author='Ken Tore Tallakstad',
    author_email='tallakstad@gmail.com',
    url='https://github.com/kentore82/pyhwschema',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

