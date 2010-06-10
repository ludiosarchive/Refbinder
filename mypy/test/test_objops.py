import unittest

import sys
from mypy import objops


class StrToNonNegTests(unittest.TestCase):

	def _call(self, s):
		return objops.strToNonNeg(s)


	def test_strToNonNeg_okay(self):
		self.assertEqual(0, self._call("0"))
		self.assertEqual(3, self._call("3"))
		self.assertEqual(12390, self._call("12390"))

		# Unicode is valid, too
		self.assertEqual(0, self._call(u"0"))
		self.assertEqual(12390, self._call(u"12390"))


	def test_strToNonNeg_TypeErrors(self):
		self.assertRaises(TypeError, lambda: self._call(None))
		self.assertRaises(TypeError, lambda: self._call([]))
		self.assertRaises(TypeError, lambda: self._call({}))


	def test_strToNonNeg_ValueErrors(self):
		# Empty str is invalid
		self.assertRaises(ValueError, lambda: self._call(""))

		# Anything with a leading zero is invalid
		self.assertRaises(ValueError, lambda: self._call("07"))
		self.assertRaises(ValueError, lambda: self._call("08"))
		self.assertRaises(ValueError, lambda: self._call("09"))
		self.assertRaises(ValueError, lambda: self._call("007"))
		self.assertRaises(ValueError, lambda: self._call("0007"))

		# Anything with non-digit character is invalid
		self.assertRaises(ValueError, lambda: self._call("-7"))
		self.assertRaises(ValueError, lambda: self._call("7e4"))
		self.assertRaises(ValueError, lambda: self._call("7.0"))
		self.assertRaises(ValueError, lambda: self._call("7."))
		self.assertRaises(ValueError, lambda: self._call("0.0"))

		# Hex is rejected
		self.assertRaises(ValueError, lambda: self._call("7f"))
		self.assertRaises(ValueError, lambda: self._call("f7"))



class StrToNonNegLimitTests(StrToNonNegTests):

	def _call(self, s, limit=2**128):
		return objops.strToNonNegLimit(s, limit)


	def test_withinLimit(self):
		self.assertEqual(0, self._call("0", 0))
		self.assertEqual(1, self._call("1", 1))
		self.assertEqual(9, self._call("9", 9))
		self.assertEqual(9, self._call("9", 10))
		self.assertEqual(2**32, self._call(str(2**32), 2**32))
		self.assertEqual(2**53, self._call(str(2**53), 2**53))
		self.assertEqual(2**65, self._call(str(2**65), 2**65))


	def test_outsideLimit(self):
		# exercise the first `num > limit:` case
		self.assertRaises(ValueError, lambda: self._call("1", 0))
		self.assertRaises(ValueError, lambda: self._call("9", 8))
		# exercise the `if len(value) > declenlimit:` case
		self.assertRaises(ValueError, lambda: self._call("999999999999999999999", 8))
		# exercise the last `num > limit:` case
		self.assertRaises(ValueError, lambda: self._call(str(2**31), 2**31 - 1))
		self.assertRaises(ValueError, lambda: self._call(str(2**53 + 1), 2**53))
		self.assertRaises(ValueError, lambda: self._call(str(2**65 + 1), 2**65))



class StrToIntInRangeTests(unittest.TestCase):

	def test_strToIntInRange_withinLimit(self):
		self.assertEqual(3, objops.strToIntInRange("3", 3, 3))
		self.assertEqual(3, objops.strToIntInRange("3", -3, 3))
		self.assertEqual(-3, objops.strToIntInRange("-3", -3, 3))
		self.assertEqual(0, objops.strToIntInRange("0", 0, 0))


	def test_strToIntInRange_outsideLimit(self):
		self.assertRaises(ValueError, lambda: objops.strToIntInRange("-4", -3, 3))
		self.assertRaises(ValueError, lambda: objops.strToIntInRange("4", -3, 3))


	def test_strToIntInRange_badNumbers(self):
		self.assertRaises(ValueError, lambda: objops.strToIntInRange("1.", -3, 3))
		self.assertRaises(ValueError, lambda: objops.strToIntInRange("1.0", -3, 3))
		self.assertRaises(ValueError, lambda: objops.strToIntInRange("1.5", -3, 3))
		self.assertRaises(ValueError, lambda: objops.strToIntInRange("-0", -3, 3))
		self.assertRaises(ValueError, lambda: objops.strToIntInRange("", -3, 3))
		self.assertRaises(ValueError, lambda: objops.strToIntInRange("x", -3, 3))
		self.assertRaises(ValueError, lambda: objops.strToIntInRange("-", -3, 3))


	def test_strToIntInRange_TypeErrors(self):
		self.assertRaises(TypeError, lambda: objops.strToIntInRange(None))
		self.assertRaises(TypeError, lambda: objops.strToIntInRange([]))
		self.assertRaises(TypeError, lambda: objops.strToIntInRange({}))



class EnsureIntTests(unittest.TestCase):

	def test_ensureInt(self):
		self.assertIs(0, objops.ensureInt(0))
		self.assertIs(-1, objops.ensureInt(-1))
		self.assertIs(-1, objops.ensureInt(-1.0))
		self.assertIs(0, objops.ensureInt(-0.0))
		self.assertIs(2, objops.ensureInt(2.0))
		self.assertEqual(200000000000000000000000000, objops.ensureInt(200000000000000000000000000))


	def test_ensureIntExceptions(self):
		self.assertRaises(ValueError, lambda: objops.ensureInt("0"))
		self.assertRaises(ValueError, lambda: objops.ensureInt("-0"))
		self.assertRaises(TypeError, lambda: objops.ensureInt({}))
		self.assertRaises(TypeError, lambda: objops.ensureInt([]))
		self.assertRaises(TypeError, lambda: objops.ensureInt(True))
		self.assertRaises(TypeError, lambda: objops.ensureInt(False))



class EnsureNonNegIntTests(unittest.TestCase):

	function = lambda _ignoredSelf, x: objops.ensureNonNegInt(x)

	def test_ensureNonNegInt(self):
		self.assertIs(0, self.function(0))
		self.assertIs(0, self.function(-0))
		self.assertIs(0, self.function(-0.0))
		self.assertIs(2, self.function(2.0))


	def test_ensureNonNegIntExceptions(self):
		self.assertRaises(ValueError, lambda: self.function(0.001))
		self.assertRaises(ValueError, lambda: self.function(-1))
		self.assertRaises(ValueError, lambda: self.function(-1.0))
		self.assertRaises(ValueError, lambda: self.function(-2.0))
		self.assertRaises(ValueError, lambda: self.function(-100000000000000000000000000000))

		self.assertRaises(TypeError, lambda: self.function("0"))
		self.assertRaises(TypeError, lambda: self.function("-0"))
		self.assertRaises(TypeError, lambda: self.function("0.001"))

		self.assertRaises(TypeError, lambda: self.function(True))
		self.assertRaises(TypeError, lambda: self.function(False))

		self.assertRaises(TypeError, lambda: self.function({}))
		self.assertRaises(TypeError, lambda: self.function([]))



class EnsureNonNegIntLimitTests(unittest.TestCase):

	function = lambda _ignoredSelf, x: objops.ensureNonNegIntLimit(x, 2**31-1)

	def test_ensureNonNegIntLimitEdgeCase(self):
		self.assertEqual(2**31 - 1, self.function(2**31 - 1))


	def test_ensureNonNegIntLimitExceptionsTooHigh(self):
		self.assertRaises(ValueError, lambda: self.function(2**31))
		self.assertRaises(ValueError, lambda: self.function(2**32))



class EnsureBoolTests(unittest.TestCase):

	def test_True(self):
		for t in (1, 1.0, True):
			self.assertEqual(True, objops.ensureBool(t))


	def test_False(self):
		for f in (0, 0.0, -0, -0.0, False):
			self.assertEqual(False, objops.ensureBool(f))


	def test_ValueError(self):
		for e in (-0.5, -1.00001, 1.0001, [], {}, set(), float('nan'), float('inf')):
			self.assertRaises(ValueError, lambda: objops.ensureBool(e))



class TotalSizeOfTests(unittest.TestCase):
	"""
	Tests for L{objops.totalSizeOf}
	"""
	def test_childlessObjects(self):
		"""
		For objects with no children,
			objops.totalSizeOf(obj) == sys.getsizeof(obj)
		"""
		s = sys.getsizeof
		self.assertEqual(s([]), objops.totalSizeOf([]))
		self.assertEqual(s({}), objops.totalSizeOf({}))
		self.assertEqual(s(1), objops.totalSizeOf(1))


	def test_listObjects(self):
		s = sys.getsizeof
		self.assertEqual(s([1]) + s(1), objops.totalSizeOf([1]))
		self.assertEqual(s([1,1,1,1]) + s(1), objops.totalSizeOf([1,1,1,1]))


	def test_dictObjects(self):
		s = sys.getsizeof

		self.assertEqual(
			s({"a": "bee"}) + s("a") + s("bee"),
			objops.totalSizeOf({"a": "bee"}))

		self.assertEqual(
			s({0: None, 1: None}) + s("a") + s("bee") + s("2") + s([None, None]),
			objops.totalSizeOf({"a": "bee", "2": ["bee", "a"]}))

		# A tuple as a dict key to make sure the implementation doesn't
		# just call sys.getsizeof on the key.
		self.assertEqual(
			s({0: None, 1: None}) + s("a") + s("bee") + s("2") + s((None, None)),
			objops.totalSizeOf({"bee": "a", ("bee", "a"): "2"}))


	def test_circularList(self):
		s = sys.getsizeof

		c = []
		c.append(c)

		n = []
		n.append(None)

		self.assertEqual(s(n), objops.totalSizeOf(c))


	def test_circularDict(self):
		s = sys.getsizeof

		c = {}
		c['key'] = c

		n = {}
		n['key'] = None

		self.assertEqual(s(n) + s('key'), objops.totalSizeOf(c))
