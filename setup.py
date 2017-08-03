#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='sensehub_client',
      version='0.1.1',
      description='Sensehub Client',
      author='Caraccio Michael and Huguenin Nicolas',
      author_email='michael.caraccio@gmail.com',
      url='-',
      install_requires=[
          "requests",
          "configparser",
      ],
      packages=find_packages(),
     )