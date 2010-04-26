from twisted.trial import unittest

from mypy.constant import GenericIdentifier, InvalidIdentifier, Constant


class _DummyId(GenericIdentifier):
	_expectedLength = 16
	__slots__ = ()



class _DummyId2(GenericIdentifier):
	_expectedLength = 16
	__slots__ = ()



class TestGenericIdentifier(unittest.TestCase):
	"""
	Tests for L{constant.GenericIdentifier}
	"""
	def test_equal(self):
		s1 = _DummyId('z' * 16)
		s2 = _DummyId('z' * 16)
		self.assertEqual(s1, s2)


	def test_notEqual(self):
		s1 = _DummyId('z' * 16)
		s2 = _DummyId('y' * 16)
		self.assertNotEqual(s1, s2)


	def test_notEqualBecauseDifferentTypes(self):
		s1 = _DummyId('a' * 16)
		self.assertNotEqual(s1, 0)
		self.assertNotEqual(0, s1)
		self.assertNotEqual(s1, 'z' * 16)

		s2 = _DummyId2('a' * 16)
		self.assertNotEqual(s1, s2)


	def test_repr(self):
		s1 = _DummyId('z' * 16)
		self.assertIn(repr('z' * 16), repr(s1))


	def test_hash(self):
		s1 = _DummyId('z' * 16)
		s2 = _DummyId('z' * 16)
		self.assertEqual(hash(s1), hash(s2))


	def test_wrongLength(self):
		self.assertRaises(InvalidIdentifier, lambda: _DummyId('z' * 15))
		self.assertRaises(InvalidIdentifier, lambda: _DummyId('z' * 17))
		self.assertRaises(InvalidIdentifier, lambda: _DummyId(''))


	def test_wrongType(self):
		self.assertRaises(TypeError, lambda: _DummyId(u'z' * 16))
		self.assertRaises(TypeError, lambda: _DummyId(u'z' * 17))
		self.assertRaises(TypeError, lambda: _DummyId(u''))
		self.assertRaises(TypeError, lambda: _DummyId(3))
		self.assertRaises(TypeError, lambda: _DummyId(3.0))
		self.assertRaises(TypeError, lambda: _DummyId(300000000000000000000000))
		self.assertRaises(TypeError, lambda: _DummyId([]))
		self.assertRaises(TypeError, lambda: _DummyId({}))
		self.assertRaises(TypeError, lambda: _DummyId(None))
		self.assertRaises(TypeError, lambda: _DummyId(True))
		self.assertRaises(TypeError, lambda: _DummyId(False))
