"""
Conversion, validation, and size measurement utilities for Python's
built-in types.
"""

import re
import sys
from math import log, log10, ceil

_postImportVars = vars().keys()


_64bitPy = sys.maxint > 2**31 - 1
_bytesPerWord = 8 if _64bitPy else 4
_gcHeaderSize = 24 if _64bitPy else 12 # Just a guess
_UCS4 = sys.maxunicode > 2**16 - 1
_bytesPerCodePoint = 4 if _UCS4 else 2

def basicGetSizeOf(obj):
	"""
	Works like L{sys.getsizeof}, but only returns reasonable numbers for
	a limited set of types: str, unicode, list, tuple, dict, set, frozenset,
	bool, NoneType, int, float, long.

	Many of these numbers are guesses.  Don't use this if L{sys.getsizeof}
	is available.
	"""
	if isinstance(obj, str):
		return _gcHeaderSize + len(obj)
	elif isinstance(obj, unicode):
		return _gcHeaderSize + _bytesPerCodePoint * len(obj)
	elif isinstance(obj, int):
		return _gcHeaderSize + _bytesPerWord
	elif isinstance(obj, float):
		return _gcHeaderSize + 8
	elif isinstance(obj, long):
		return _gcHeaderSize + int(ceil(log(obj, 2)))
	elif isinstance(obj, (list, tuple)):
		return _gcHeaderSize + _bytesPerWord + _bytesPerWord * len(obj)
	elif isinstance(obj, dict):
		return _gcHeaderSize + _bytesPerWord * (750 + 8 * len(obj))
	elif isinstance(obj, (set, frozenset)):
		return _gcHeaderSize + _bytesPerWord * (750 + 5 * len(obj))
	else:
		return _gcHeaderSize + _bytesPerWord
	# TODO: handle C{complex}es

try:
	from sys import getsizeof
except ImportError:
	getsizeof = basicGetSizeOf


# Neither of these accept "-0"
_OKAY_NONNEG_INT = re.compile(r'^(0|[1-9]\d*)$')
_OKAY_INT = re.compile(r'^(0|\-?[1-9]\d*)$')

def strToNonNeg(value):
	"""
	A very strict numeric-string to non-zero integer converter.
	This should help prevent people from developing buggy clients
	that just happen to work with our current server.

	We don't use Python's int() because it allows a lot of things,
	including int('-0') and int(' -0').

	Raises C{ValueError} if negative.
	"""
	if _OKAY_NONNEG_INT.match(value):
		return int(value)

	raise ValueError("could not decode to non-negative integer: %r" % (value,))


def strToNonNegLimit(value, limit):
	"""
	Like L{strToNonNeg}, except with a numerical limit C{limit}.

	Raises C{ValueError} if too high (or negative).
	"""
	# Optimizations for the common case
	if limit == 2**53:
		declenlimit = 16
	elif limit == 2**31 - 1:
		declenlimit = 10
	else:
		declenlimit = int(log10(limit) + 1) if limit != 0 else 1

	if len(value) > declenlimit:
		raise ValueError("too high")

	if _OKAY_NONNEG_INT.match(value):
		num = int(value)
		if num > limit:
			raise ValueError("too high")
		return num

	raise ValueError("could not decode to non-negative integer: %r" % (value,))


def strToIntInRange(value, lower, upper):
	"""
	A very strict numeric-string to integer converter.

	@rtype: L{int} or L{long}
	@return: C{value} as converted from a str to an int/long.

	Raises C{ValueError} if too high or too low.
	"""
	if _OKAY_INT.match(value):
		num = int(value)
	else:
		raise ValueError("value %r does not look numeric" % (value,))

	if not lower <= num <= upper:
		raise ValueError("value %r not in range [%r, %r]" % (value, lower, upper))

	return num


def ensureInt(value):
	"""
	Convert C{value} from a L{float} to an equivalent L{int}/L{long} if
	possible, else raise L{ValueError}. C{int}s and C{long}s pass through.

	@rtype: L{int} or L{long}
	@return: non-float equivalent of C{value}
	"""
	if value is True or value is False:
		raise TypeError("Even though int(False) and int(True) work, we disallow it.")
	inted = int(value)
	if inted != value:
		raise ValueError("%r cannot be converted to identical integer" % (value,))
	return inted


def ensureNonNegInt(value):
	"""
	Check that C{value} is non-negative and convert it to it an equivalent
	non-L{float} if necessary, else raise L{ValueError}.

	@rtype: L{int} or L{long}
	@return: non-float equivalent of C{value}

	Useful after getting some deserialized JSON with random stuff in it.
	"""

	if isinstance(value, (int, long, float)) and value is not True and value is not False:
		if value < 0:
			raise ValueError("%r is < 0" % (value,))
		elif isinstance(value, float):
			return ensureInt(value)
		else:
			return value
	else:
		raise TypeError("%r is not an int/long/float" % (value,))


def ensureNonNegIntLimit(value, limit):
	"""
	Check that C{value} is non-negative and C{<= limit} and
	convert it to it an equivalent non-L{float} if necessary, else raise L{ValueError}.

	@rtype: L{int} or L{long}
	@return: non-float equivalent of C{value}

	Useful after getting some deserialized JSON with random stuff in it.
	"""
	v = ensureNonNegInt(value)
	if v > limit:
		raise ValueError("%r is > limit %r" % (value, limit))
	return v


def ensureBool(value):
	"""
	Convert 1, 1.0, and True to True.
	Convert 0, 0.0, -0.0, and False to False.
	For all other values, raise L{ValueError}.

	@rtype: L{bool}
	@return: non-number equivalent of C{value}

	This is useful when getting JSON-decoded values from a peer, and you
	do not want to keep their bool-equivalent numbers around in memory.
	"""
	if value == True:
		return True
	elif value == False:
		return False
	else:
		raise ValueError("%r is not bool-equivalent to True or False" % (value,))


def totalSizeOf(obj, _alreadySeen=None):
	"""
	Get the size of object C{obj} using L{sys.getsizeof} or L{basicGetSizeOf}
	on the object itself and all of its children recursively.  If the same
	object appears more than once inside C{obj}, it is counted only once.

	This only works properly if C{obj} is a str, unicode, list, tuple, dict,
	set, frozenset, bool, NoneType, int, complex, float, long, or any nested
	combination of the above.  C{obj} is allowed to have circular references.

	This is particularly useful for getting a good estimate of how much
	memory a JSON-decoded object is using after receiving it.

	Design notes: L{sys.getsizeof} or L{basicGetSizeOf} return reasonable
	numbers, but do not recurse into the object's children.  As we recurse
	into the children, we keep track of objects we've already counted for two
	reasons:
		- If we've already counted the object's memory usage, we don't
		want to count it again.
		- As a bonus, we handle circular references gracefully.

	This function assumes that containers do not modify their children as
	they are traversed.

	If your Python is < 2.6, the returned size will be less accurate, because
	L{basicGetSizeOf} is used instead of L{sys.getsizeof}.
	"""
	if _alreadySeen is None:
		_alreadySeen = set()

	total = getsizeof(obj)
	_alreadySeen.add(id(obj))

	if isinstance(obj, dict):
		# Count the memory usage of both the keys and values.
		for k, v in obj.iteritems():
			if not id(k) in _alreadySeen:
				total += totalSizeOf(k, _alreadySeen)
			if not id(v) in _alreadySeen:
				total += totalSizeOf(v, _alreadySeen)
	else:
		try:
			iterator = obj.__iter__()
		except (TypeError, AttributeError):
			pass
		else:
			for item in iterator:
				if not id(item) in _alreadySeen:
					total += totalSizeOf(item, _alreadySeen)

	return total


from mypy import refbinder
refbinder.bindRecursive(sys.modules[__name__], _postImportVars)
del refbinder
