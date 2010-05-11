from twisted.trial import unittest

from mypy.dictops import frozendict


class FrozenDictTests(unittest.TestCase):

	def test_hashable(self):
		d = frozendict(x=3, y=(), z="string")
		self.assertTrue(isinstance(hash(d), int))
		# exercise _cachedHash
		self.assertTrue(isinstance(hash(d), int))


	def test_notHashable(self):
		d = frozendict(x=[])
		# exceptions.TypeError: unhashable type: 'list'
		self.assertRaises(TypeError, lambda: hash(d))


	def test_repr(self):
		d = frozendict(x=3)
		self.assertEqual("frozendict({'x': 3})", repr(d))


	def test_reprEmpty(self):
		d = frozendict()
		self.assertEqual("frozendict({})", repr(d))


	def test_equality(self):
		self.assertEqual(frozendict(), frozendict())
		self.assertEqual(frozendict(x=3), frozendict(x=3))
		self.assertNotEqual(frozendict(x=3), frozendict(x=4))


	def test_immutable(self):
		def delete(obj, key):
			del obj[key]

		def set(obj, key, value):
			obj[key] = value

		d = frozendict(x=3)
		self.assertRaises(AttributeError, lambda: d.pop())
		self.assertRaises(AttributeError, lambda: d.popitem())
		self.assertRaises(AttributeError, lambda: d.clear())
		self.assertRaises(AttributeError, lambda: delete(d, "x"))
		self.assertRaises(AttributeError, lambda: set(d, "x", 4))
		self.assertRaises(AttributeError, lambda: d.setdefault("x", "y"))
		self.assertRaises(AttributeError, lambda: d.update({"x": 4}))


	def test_callingInitDoesNotUpdate(self):
		"""
		You can do this to Python dictionaries:

		>>> d = {1: 2}
		>>> d
		{1: 2}
		>>> d.__init__({1: 3})
		>>> d
		{1: 3}

		We don't waste a slot on frozendict to strategically throw
		AttributeError; we assume people calling __init__ a second time
		are insane and just ignore their request.

		Make sure that __init__ can't mutate the dict, though.
		"""
		d = frozendict(x=3)
		d.__init__({"x": 4})
		self.assertEqual(3, d['x'])
