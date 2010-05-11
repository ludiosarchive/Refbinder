from twisted.trial import unittest

from mypy.constant import (
	BaseConstant, Constant, GenericIdentifier, InvalidIdentifier)


class AnyConstant(BaseConstant):
	__slots__ = ()

	@classmethod
	def preCheck(cls, value):
		pass



class AnyConstant2(BaseConstant):
	__slots__ = ()

	@classmethod
	def preCheck(cls, value):
		pass



class DummyId(GenericIdentifier):
	_expectedLength = 16
	__slots__ = ()



class BaseConstantTests(unittest.TestCase):
	"""
	Tests for L{constant.BaseConstant}
	"""
	def test_equal(self):
		s1 = AnyConstant('z' * 16)
		s2 = AnyConstant('z' * 16)
		self.assertEqual(s1, s2)


	def test_notEqual(self):
		s1 = AnyConstant('z' * 16)
		s2 = AnyConstant('y' * 16)
		self.assertNotEqual(s1, s2)


	def test_notEqualBecauseDifferentTypes(self):
		s1 = AnyConstant('a' * 16)
		self.assertNotEqual(s1, 0)
		self.assertNotEqual(0, s1)
		self.assertNotEqual(s1, 'z' * 16)

		s2 = AnyConstant2('a' * 16)
		self.assertNotEqual(s1, s2)


	def test_repr(self):
		s1 = AnyConstant('z' * 16)
		self.assertIn(repr('z' * 16), repr(s1))


	def test_hash(self):
		s1 = AnyConstant('z' * 16)
		s2 = AnyConstant('z' * 16)
		self.assertEqual(hash(s1), hash(s2))


	def test_reachValue(self):
		s1 = AnyConstant('z')
		self.assertEqual('z', s1.value)

		self.assertRaises((TypeError, AttributeError), lambda: s1.notAnAttr)



class ConstantTests(unittest.TestCase):
	"""
	Tests for L{constant.Constant}
	"""
	def test_wrongType(self):
		self.assertRaises(TypeError, lambda: Constant(u'z' * 16))
		self.assertRaises(TypeError, lambda: Constant(u'z' * 17))
		self.assertRaises(TypeError, lambda: Constant(u''))
		self.assertRaises(TypeError, lambda: Constant(3))
		self.assertRaises(TypeError, lambda: Constant(3.0))
		self.assertRaises(TypeError, lambda: Constant(300000000000000000000000))
		self.assertRaises(TypeError, lambda: Constant([]))
		self.assertRaises(TypeError, lambda: Constant({}))
		self.assertRaises(TypeError, lambda: Constant(None))
		self.assertRaises(TypeError, lambda: Constant(True))
		self.assertRaises(TypeError, lambda: Constant(False))



class GenericIdentifierTests(unittest.TestCase):
	"""
	Tests for L{constant.GenericIdentifier}
	"""
	def test_wrongLength(self):
		self.assertRaises(InvalidIdentifier, lambda: DummyId('z' * 15))
		self.assertRaises(InvalidIdentifier, lambda: DummyId('z' * 17))
		self.assertRaises(InvalidIdentifier, lambda: DummyId(''))


	def test_wrongType(self):
		self.assertRaises(TypeError, lambda: Constant(u'z' * 16))
