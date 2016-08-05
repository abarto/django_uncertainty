#!/usr/bin/env python

from setuptools import setup

setup(name='django_uncertainty',
      version='0.1',
      description='A Django application to generate predictable errors on sites',
      author='Agustin Barto',
      author_email='abarto@gmail.com',
      url='https://github.com/abarto/django_uncertainty',
      install_requires=[],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Framework :: Django :: 1.10',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities',
      ],
      packages=['uncertainty'])
