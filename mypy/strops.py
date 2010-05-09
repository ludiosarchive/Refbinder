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
			self.__class__.__name__, id(self[0]), self[1], self[2])


	def toBuffer(self):
		"""
		Return a C{buffer} object for the fragment. Note that Python
		will not collect the underlying string object if there is a buffer
		of it.
		"""
		return buffer(self[0], self[1], self[2])


	# TODO: toMemoryview

	def toString(self):
		pos = self[1]
		return self[0][pos:pos+self[2]]


	# We're not equal to constants of another class
	def __eq__(self, other):
		return False if type(self) != type(other) else self.toBuffer() == other.toBuffer()


	def __ne__(self, other):
		return True if type(self) != type(other) else self.toBuffer() != other.toBuffer()



from pypycpyo import optimizer
optimizer.bind_all_many(vars(), _postImportVars)
