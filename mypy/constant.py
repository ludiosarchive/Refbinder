_postImportVars = vars().keys()


class BaseConstant(tuple):
	"""
	Base class for defining constants. Immutable.
	"""
	__slots__ = ()

	def __new__(cls, value):
		cls.preCheck(value)
		return tuple.__new__(cls, (value,))


	def __repr__(self):
		return '%s(%r)' % (self.__class__.__name__, self[0])


	# We're not equal to constants of another class
	def __eq__(self, other):
		return False if type(self) != type(other) else self[0] == other[0]


	def __ne__(self, other):
		return True if type(self) != type(other) else self[0] != other[0]


	@classmethod
	def preCheck(cls, value):
		raise NotImplementedError("Override preCheck")



class Constant(BaseConstant):
	"""
	Represents a string constant. Immutable.
	"""
	__slots__ = ()

	@classmethod
	def preCheck(cls, value):
		if not isinstance(value, str):
			raise TypeError("value must be a str, was %r" % (type(value),))



class InvalidIdentifier(Exception):
	pass



class GenericIdentifier(Constant):
	__slots__ = ()

	_expectedLength = -1

	@classmethod
	def preCheck(cls, value):
		Constant.preCheck(value)
		length = len(value)
		if length != cls._expectedLength:
			raise InvalidIdentifier("id must be of length %d; was %d" % (cls._expectedLength, length))



from pypycpyo import optimizer
optimizer.bind_all_many(vars(), _postImportVars)
