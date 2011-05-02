Overview
========

Mypy is a collection of Python utilities that are usable in a wide variety
of applications.

To install:
$ python setup.py install

To run the tests, first install Twisted, then:
$ trial mypy


Modules
=======

mypy.complainer
	`complainImplicitUnicodeConversions(True)` will make Python complain
	about implicit unicode/str conversions.  This is a high-level interface
	for washort's ascii_with_complaints.

mypy.constant
	`Constant` is useful for representing symbolic constants.

mypy.dictops
	`securedict` behaves almost exactly like `dict` but is (probably)
	safe against an algorithmic complexity attack where keys with colliding
	hashes are inserted into a dict.

	`consensualfrozendict` is a `dict` but blocks naive attempts to mutate
	it.

mypy.filecache
	`FileCache` is useful for caching file resources that never change over
	the lifetime of the program.

mypy.imgops
	`pngSize` and `gifSize` returns the dimensions of png/gif file object.

mypy.iterops
	`areAllEqual` returns True if all items in iterable are equal.

mypy.objops
	`totalSizeOf` returns an estimate of how much memory an object uses.

	Contains several other functions useful for checking what the
	type/value of objects you received over the wire.

mypy.randgen
	`RandomFactory` can give you random bytes without calling `os.urandom`
	every time; it caches `bufferSize` bytes.

mypy.refbinder
	Contains a high-level interface for mypy._refbinder, which is mostly
	Raymond Hettinger's "Decorator for BindingConstants at compile time"

mypy.strops
	`rreplace` performs one right-replace.

	`StringFragment` represents a string fragment.  Useful if you want to
	avoid copying when passing just part of a string.

	`slowStringCompare` can compare two `str`s without returning early
	at the first mismatching byte.  This can help you avoid timing attacks
	when comparing equal-length passwords.

mypy.testhelpers
	`ReallyEqualMixin` provides two test methods that exercise all of
	__eq__, __ne__, and __cmp__.  This prevents a common bug where you
	forget to define __ne__.


TODO
====

* Consider making securedict not a dict, given that dict(aSecureDict)
  does not work correctly in CPython.  Maybe use UserDict?

* Add method to FileCache that yields every entry in the cache.

* Fix or remove mypy.dictops.frozendict


Code style notes
================

This package mostly follows the Divmod Coding Standard
<http://replay.web.archive.org/20090118191929/http://divmod.org/trac/wiki/CodingStandard>,
except:

* Use hard tabs for indentation.
* Use hard tabs only at the beginning of a line.
* Prefer to have lines <= 80 characters, but always less than 100.
  In docstrings, use epytext.
