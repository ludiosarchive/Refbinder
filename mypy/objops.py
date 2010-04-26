"""
Conversion, validation, and size measurement utilities for Python's
built-in types.
"""

import re
from sys import getsizeof

_postImportVars = vars().keys()


_quickConvert_strToPosInt = {}
for num in xrange(10000):
	_quickConvert_strToPosInt[str(num)] = num

_OKAY_NUMBER = re.compile(r'^[1-9]\d*$')
def strToNonNeg(value):
	"""
	A very strict numeric-string to non-zero integer converter.
	This should help prevent people from developing buggy clients
	that just happen to work with our current server.

	We don't use Python's int() because it allows a lot of things,
	including int('-0') and int(' -0').
	"""

	# TODO: This (probably) makes things faster, but we need a benchmark to know for sure.
	quick = _quickConvert_strToPosInt.get(value)
	if quick is not None:
		return quick
	if _OKAY_NUMBER.match(value):
		return int(value)

	raise ValueError("could not decode to non-negative integer: %r" % (value,))


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
	Convert 1.0, 1, and True to True.
	Convert 0.0, 0, -0.0, -0, and False to False.
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
	Get the size of object C{obj} using C{sys.getsizeof} on the object itself
	and all of its children recursively. If the same object appears more
	than once inside C{obj}, it is counted only once.

	This only works properly if C{obj} is a str, unicode, list, dict, set,
	bool, NoneType, int, complex, float, long, or any nested combination
	of the above. C{obj} is allowed to have circular references.

	This is particularly useful for getting a good estimate of how much
	memory a JSON-decoded object is using after receiving it.

	Design notes: sys.getsizeof seems to return very accurate numbers,
	but does not recurse into the object's children. As we recurse into
	the children, we keep track of objects we've already counted for two
	reasons:
		- If we've already counted the object's memory usage, we don't
		want to count it again.
		- As a bonus, we handle circular references gracefully.

	This function assumes that containers do not modify their children as
	they are traversed.
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


from pypycpyo import optimizer
optimizer.bind_all_many(vars(), _postImportVars)
