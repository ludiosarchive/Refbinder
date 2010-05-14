"""
Basic string operations that should have been in Python.
"""

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


	# We're not equal to constants of another class
	def __eq__(self, other):
		return False if type(self) != type(other) else self.toBuffer() == other.toBuffer()


	def __ne__(self, other):
		return True if type(self) != type(other) else self.toBuffer() != other.toBuffer()



from pypycpyo import optimizer
optimizer.bind_all_many(vars(), _postImportVars)
