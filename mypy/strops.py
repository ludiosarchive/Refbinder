"""
Basic string operations that should have been in Python.
"""

import sys
import warnings

_postImportVars = vars().keys()


def rreplace(string, needle, replacement):
	"""
	If needle in string,
		replace the last instance of L{needle} in L{string} with L{replacement}
	else,
		return the original L{string}
	"""

	location = string.rfind(needle)

	if location == -1:
		return string

	return (string[:location] + replacement + string[location + len(needle):])



class StringFragment(object):
	"""
	Represents a fragment of a string. Used to avoid copying, especially in
	network protocols.

	DO NOT adjust the attributes of the object after you instantiate it; this
	is faux-immutable.

	You can slice a L{StringFragment}, which will return a new
	L{StringFragment}. You can index it, which will return a 1-byte C{str}.

	Equal and hash-equivalent to other L{StringFragment}s that represent
	the same string fragment.
	"""
	__slots__ = ('_string', '_pos', 'size')

	def __init__(self, string, pos, size):
		self._string = string
		self._pos = pos
		self.size = size


	def __repr__(self):
		return '<%s for 0x%x, pos=%r, size=%r, represents %r>' % (
			self.__class__.__name__, id(self._string), self._pos, self.size, str(self))


	def __len__(self):
		# Note: __len__ needs to be implemented for another
		# reason: so that __getslice__ works properly when sliced
		# with negative numbers.
		return self.size


	def __getitem__(self, num):
		# Unlike for __getslice__, Python passes through negative numbers
		# to __getitem__.

		pos = self._pos
		size = self.size
		rightLimit = pos + size - 1

		if num < 0:
			num = size + num
		num = pos + num
		if not pos <= num <= rightLimit:
			raise IndexError("StringFragment index out of range")

		return self._string[num]


	def __getslice__(self, start, end):
		##print self, start, end
		maximumLength = min(self.size - start, end - start)
		newStart = self._pos + start
		##print newStart, maximumLength
		return StringFragment(self._string, newStart, max(0, maximumLength))


	# TODO: toMemoryview # Python does not provide a __memoryview__

	def toBuffer(self): # Python does not provide a __buffer__
		"""
		Return a C{buffer} object for the fragment. Note that Python
		will not collect the underlying string object if there is a buffer
		of it.
		"""
		return buffer(self._string, self._pos, self.size)


	def __str__(self):
		pos = self._pos
		return self._string[pos:pos+self.size]


	def __hash__(self):
		return hash(self.toBuffer())


	def __eq__(self, other):
		return False if type(self) != type(other) else self.toBuffer() == other.toBuffer()


	def __ne__(self, other):
		return True if type(self) != type(other) else self.toBuffer() != other.toBuffer()



def slowStringCompare(s1, s2):
	"""
	Compare C{s1} and C{s2} for equality, but always take
	the same amount of time when both strings are of the same length.
	This is intended to stop U{timing attacks<http://rdist.root.org/2009/05/28/timing-attack-in-google-keyczar-library/>}.

	This implementation should do what keyczar does::

	  - http://code.google.com/p/keyczar/source/browse/trunk/python/src/keyczar/keys.py?r=471#352
	  - http://rdist.root.org/2010/01/07/timing-independent-array-comparison/

	@param s1: string to compare to s2
	@type s1: C{str}

	@param s2: string to compare to s1
	@type s2: C{str}

	@return: C{True} if strings are equivalent, else C{False}.
	@rtype: C{bool}

	@warning: if C{s1} and C{s2} are of unequal length, the comparison will take
		less time.  An attacker may be able to guess how long the expected
		string is.  To avoid this problem, compare only fixed-length hashes.
	"""
	if isinstance(s1, unicode) or isinstance(s2, unicode):
		warnings.warn(
			"Passing unicode strings to slowStringCompare is insecure",
			DeprecationWarning,
			stacklevel=2)

	if isinstance(s1, unicode) and not isinstance(s2, unicode):
		try:
			s2 = unicode(s2)
		except UnicodeDecodeError:
			if sys.version_info < (2, 5):
				# When Python 2.4 cannot decode the non-unicode side of a
				# string comparion, it raises UnicodeDecodeError instead of
				# giving a UnicodeWarning and returning False.  Match this
				# behavior and re-raise the exception.
				raise
			return False
	elif not isinstance(s1, unicode) and isinstance(s2, unicode):
		try:
			s1 = unicode(s1)
		except UnicodeDecodeError:
			if sys.version_info < (2, 5):
				raise
			return False

	if len(s1) != len(s2):
		return False
	result = 0
	for n in xrange(len(s1)):
		result |= ord(s1[n]) ^ ord(s2[n])
	return result == 0



from mypy import refbinder
refbinder.bindRecursive(sys.modules[__name__], _postImportVars)
del refbinder
