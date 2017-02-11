#!/usr/bin/env python

from os import path
from setuptools import setup


with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst')) as f:
    long_description = f.read()


setup(name='django_uncertainty',
      version='1.6',
      description='A Django middleware to generate predictable errors on sites',
      long_description=long_description,
      author='Agustin Barto',
      author_email='abarto@gmail.com',
      url='https://github.com/abarto/django_uncertainty',
      license='BSD',
      install_requires=[],
      tests_require=['Django>=1.10'],
      test_suite='uncertainty.tests.runtests.runtests',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities',
      ],
      packages=['uncertainty'])
