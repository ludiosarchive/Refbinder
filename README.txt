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

- Fix or remove mypy.dictops.frozendict


Code style notes
================

This package mostly follows the Divmod Coding Standard:
	http://divmod.org/trac/wiki/CodingStandard
except:
-	Use hard tabs for indentation.
-	Use hard tabs only at the beginning of a line.
-	Prefer to have lines <= 80 characters, but always less than 100.
-	In docstrings, use epytext.
