Overview
========

Mypy is a collection of Python utilities that are usable in a wide variety
of applications.

TODO: describe each module here

To install:
$ python setup.py install

To run the tests, first install Twisted, then:
$ trial mypy


TODO list
=========

- Consider making securedict not a dict, given that dict(aSecureDict)
  does not work correctly in CPython.  Maybe use UserDict?

- Add method to FileCache that yields every entry in the cache.

- Move pypycpyo.optimizer to mypy, or remove all uses of it.

- Fix or remove mypy.dictops.frozendict
