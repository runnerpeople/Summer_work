#!/usr/bin/env python

from distutils.core import setup

setup(name='T-bmstu',
      version='1.0',
      description='Автоматический тестер решения задач в системе тестирования T-bmstu',
      author='Runner People',
      url='http://www.github.com/runnerpeople/Summer_work/tree/master/T-bmstu',
      scripts=["tester.py"],
      data_files=["tests.txt"],
      license="IU9")
