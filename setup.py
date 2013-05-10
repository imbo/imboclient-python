# coding=utf-8
from setuptools import setup

setup(
        name='imbo',
        version='0.0.1',
        author='Andreas Søvik',
        author_email='arsovik@gmail.com',
        packages=['imboclient'],
        scripts=[],
        url='http://www.imbo-project.org',
        license='LICENSE.txt',
        description='Python client for Imbo',
        long_description=open('README.md').read(),
        install_requires=['requests', 'nose', 'mock'],
)

