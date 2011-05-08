Mypy overview
=============

Mypy is a collection of Python utilities that are usable in a wide variety
of applications.


Installation
============

`python setup.py install`

This installs the module `mypy`.


Modules
=======

__mypy.complainer__

`complainImplicitUnicodeConversions(True)` will make Python complain
about implicit unicode/str conversions.  This is a high-level interface
for washort's `ascii_with_complaints`.

__mypy.constant__

`Constant` is useful for representing symbolic constants.

__mypy.dictops__

`consensualfrozendict` is a `dict` but blocks naive attempts to mutate
it.

__mypy.filecache__

`FileCache` is useful for caching file resources that never change over
the lifetime of the program.

__mypy.imgops__

`pngSize` and `gifSize` returns the dimensions of png/gif file object.

__mypy.iterops__

`areAllEqual` returns True if all items in iterable are equal.

__mypy.objops__

`totalSizeOf` returns an estimate of how much memory an object uses.

Contains several other functions useful for checking what the
type/value of objects you received over the wire.

__mypy.randgen__

`RandomFactory` can give you random bytes without calling `os.urandom`
every time; it caches `bufferSize` bytes.

__mypy.refbinder__

Contains a high-level interface for `mypy._refbinder`, which is mostly
Raymond Hettinger's "Decorator for BindingConstants at compile time"

__mypy.strops__

`rreplace` performs one right-replace.

`StringFragment` represents a string fragment.  Useful if you want to
avoid copying when passing just part of a string.

`slowStringCompare` can compare two `str`s without returning early
at the first mismatching byte.  This can help you avoid timing attacks
when comparing equal-length passwords.

__mypy.testhelpers__

`ReallyEqualMixin` provides two test methods that exercise all of
`__eq__`, `__ne__`, and `__cmp__`.  This prevents a common bug where you
forget to define `__ne__`.


Running the tests
=================

Install Twisted, then run `trial mypy`


TODO
====

*	Add method to `FileCache` that yields every entry in the cache.


Code style notes
================

This package mostly follows the Divmod Coding Standard
<http://replay.web.archive.org/http://divmod.org/trac/wiki/CodingStandard> with a few exceptions:

*	Use hard tabs for indentation.

*	Use hard tabs only at the beginning of a line.

*	Prefer to have lines <= 80 characters, but always less than 100.
