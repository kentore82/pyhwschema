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
    version='0.0.1',
    install_requires=requirements,
    extras_require={
        ':python_version == "2.7"': [
            'avro',
        ],
        ':python_version >= "3.0"': [
            'avro-python3',
        ],
    },
    description='Python API for Hortonworks Schema Registry',
    long_description=readme,
    author='Ken Tore Tallakstad',
    author_email='tallakstad@gmail.com',
    url='https://github.com/kentore82/pyhwschema',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

