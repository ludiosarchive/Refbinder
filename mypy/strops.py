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



class StringFragment(tuple):
	"""
	Represents a fragment of a string. Used to avoid copying, especially in
	network protocols.

	You can slice a L{StringFragment}, but you cannot index it. (Indexes
	are reserved for grabbing

	Equal to other L{StringFragment}s that represent the same string
	fragment. Not necessarily hash-equivalent to such L{StringFragment}s,
	though.
	"""
	__slots__ = ()

	def __new__(cls, string, pos, size):
		"""
		C{string} is a C{str} object.
		C{pos} is the position the fragment starts at.
		C{size} is the size of the fragment.
		"""
		return tuple.__new__(cls, (string, pos, size))


	def __repr__(self):
		return '<%s for object at 0x%x, pos=%r, size=%r>' % (
			self.__class__.__name__, id(self[FS_STR]), self[FS_POSITION], self[FS_SIZE])


	def __len__(self):
		# Note: __len__ needs to be implemented for another
		# reason: so that __getslice__ works properly when sliced
		# with negative numbers.
		return self[FS_SIZE]


	def __getslice__(self, start, end):
		##print self, start, end
		maximumLength = min(self[FS_SIZE] - start, end - start)
		newStart = self[FS_POSITION] + start
		##print newStart, maximumLength
		return StringFragment(self[FS_STR], newStart, max(0, maximumLength))


	# TODO: toMemoryview # Python does not provide a __memoryview__

	def toBuffer(self): # Python does not provide a __buffer__
		"""
		Return a C{buffer} object for the fragment. Note that Python
		will not collect the underlying string object if there is a buffer
		of it.
		"""
		return buffer(self[FS_STR], self[FS_POSITION], self[FS_SIZE])


	def __str__(self):
		pos = self[FS_POSITION]
		return self[FS_STR][pos:pos+self[FS_SIZE]]


	# We're not equal to constants of another class
	def __eq__(self, other):
		return False if type(self) != type(other) else self.toBuffer() == other.toBuffer()


	def __ne__(self, other):
		return True if type(self) != type(other) else self.toBuffer() != other.toBuffer()


# These are public, feel free to use them.

FS_STR = 0
FS_POSITION = 1
FS_SIZE = 2


from pypycpyo import optimizer
optimizer.bind_all_many(vars(), _postImportVars)
