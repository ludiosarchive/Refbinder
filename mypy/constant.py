import types
import operator

_postImportVars = vars().keys()


class _MarkerAttacher(type):
	def __new__(meta, class_name, bases, new_attrs):
		cls = type.__new__(meta, class_name, bases, new_attrs)
		setattr(cls, meta._attrName, object())
		return cls



def attachClassMarker(attrName):
	"""
	A function that returns a metaclass that attaches a unique and
	hashable marker to the class. C{attrName} is the name for the
	marker attribute (on the class).

	This is useful for immutable types that subclass tuple and
	want a marker as the first item of the tuple, to make different
	types not equal to each other.

	You may be surprised to learn that an object() hashes and
	is immutable.

	Sample usage:

	class MyImmutable(tuple):
		__slots__ = ()
		__metaclass__ = MarkerAttacher('_MARKER')

		def __new__(cls, value):
			cls.preCheck(value)
			return tuple.__new__(cls, (cls._MARKER, value))
	"""
	metaclass = types.ClassType('_MarkerAttacher_' + attrName, (_MarkerAttacher,), {})
	metaclass._attrName = attrName
	return metaclass



class BaseConstant(tuple):
	"""
	Base class for defining constants. Immutable.

	We could have used __eq__ and __ne__ to make different types
	non-equal, but a marker as the first element is probably faster.
	"""
	__slots__ = ()
	__metaclass__ = attachClassMarker('_MARKER')

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



try:
	from pypycpyo import optimizer
except ImportError:
	pass
else:
	optimizer.bind_all_many(vars(), _postImportVars)
