import operator

_postImportVars = vars().keys()


class MarkerAttacher(type):
	"""
	A metaclass that attaches a unique and hashable marker to the class.

	This is useful for immutable types that subclass tuple and
	want a marker as the first item of the tuple to make different
	types not equal to each other.

	You may be surprised to learn that an object() hashes and
	is immutable.
	"""
	def __new__(meta, class_name, bases, new_attrs):
		cls = type.__new__(meta, class_name, bases, new_attrs)
		cls._MARKER = object()
		return cls



class BaseConstant(tuple):
	"""
	Base class for defining constants. Immutable.

	We could have used __eq__ and __ne__ to make different types
	non-equal, but a marker as the first element is probably faster.
	"""
	__slots__ = ()
	__metaclass__ = MarkerAttacher

	value = property(operator.itemgetter(1))

	def __new__(cls, value):
		cls.preCheck(value)
		return tuple.__new__(cls, (cls._MARKER, value))


	def __repr__(self):
		return '%s(%r)' % (self.__class__.__name__, self[1])


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
