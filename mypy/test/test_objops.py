from twisted.trial import unittest

from mypy import objops


class TestStrToNonNeg(unittest.TestCase):

	def test_strToNonNeg_okay(self):
		self.assertEqual(0, objops.strToNonNeg("0"))
		self.assertEqual(3, objops.strToNonNeg("3"))
		self.assertEqual(12390, objops.strToNonNeg("12390"))

		# Unicode is valid, too
		self.assertEqual(0, objops.strToNonNeg(u"0"))
		self.assertEqual(12390, objops.strToNonNeg(u"12390"))


	def test_strToNonNeg_TypeErrors(self):
		self.assertRaises(TypeError, lambda: objops.strToNonNeg(None))
		self.assertRaises(TypeError, lambda: objops.strToNonNeg([]))
		self.assertRaises(TypeError, lambda: objops.strToNonNeg({}))


	def test_strToNonNeg_ValueErrors(self):
		# Empty str is invalid
		self.assertRaises(ValueError, lambda: objops.strToNonNeg(""))

		# Anything with a leading zero is invalid
		self.assertRaises(ValueError, lambda: objops.strToNonNeg("07"))
		self.assertRaises(ValueError, lambda: objops.strToNonNeg("08"))
		self.assertRaises(ValueError, lambda: objops.strToNonNeg("09"))
		self.assertRaises(ValueError, lambda: objops.strToNonNeg("007"))
		self.assertRaises(ValueError, lambda: objops.strToNonNeg("0007"))

		# Anything with non-digit character is invalid
		self.assertRaises(ValueError, lambda: objops.strToNonNeg("-7"))
		self.assertRaises(ValueError, lambda: objops.strToNonNeg("7e4"))
		self.assertRaises(ValueError, lambda: objops.strToNonNeg("7.0"))
		self.assertRaises(ValueError, lambda: objops.strToNonNeg("7."))
		self.assertRaises(ValueError, lambda: objops.strToNonNeg("0.0"))

		# Hex is rejected
		self.assertRaises(ValueError, lambda: objops.strToNonNeg("7f"))
		self.assertRaises(ValueError, lambda: objops.strToNonNeg("f7"))



class TestEnsureInt(unittest.TestCase):

	def test_ensureInt(self):
		self.assertIdentical(0, objops.ensureInt(0))
		self.assertIdentical(-1, objops.ensureInt(-1))
		self.assertIdentical(-1, objops.ensureInt(-1.0))
		self.assertIdentical(0, objops.ensureInt(-0.0))
		self.assertIdentical(2, objops.ensureInt(2.0))
		self.assertEqual(200000000000000000000000000, objops.ensureInt(200000000000000000000000000))


	def test_ensureIntExceptions(self):
		self.assertRaises(ValueError, lambda: objops.ensureInt("0"))
		self.assertRaises(ValueError, lambda: objops.ensureInt("-0"))
		self.assertRaises(TypeError, lambda: objops.ensureInt({}))
		self.assertRaises(TypeError, lambda: objops.ensureInt([]))
		self.assertRaises(TypeError, lambda: objops.ensureInt(True))
		self.assertRaises(TypeError, lambda: objops.ensureInt(False))



class TestEnsureNonNegInt(unittest.TestCase):

	function = lambda _ignoredSelf, x: objops.ensureNonNegInt(x)

	def test_ensureNonNegInt(self):
		self.assertIdentical(0, self.function(0))
		self.assertIdentical(0, self.function(-0))
		self.assertIdentical(0, self.function(-0.0))
		self.assertIdentical(2, self.function(2.0))


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



class TestEnsureNonNegIntLimit(unittest.TestCase):

	function = lambda _ignoredSelf, x: objops.ensureNonNegIntLimit(x, 2**31-1)

	def test_ensureNonNegIntLimitEdgeCase(self):
		self.assertEqual(2**31 - 1, self.function(2**31 - 1))


	def test_ensureNonNegIntLimitExceptionsTooHigh(self):
		self.assertRaises(ValueError, lambda: self.function(2**31))
		self.assertRaises(ValueError, lambda: self.function(2**32))



class TestEnsureBool(unittest.TestCase):

	def test_True(self):
		for t in (1, 1.0, True):
			self.aE(True, objops.ensureBool(t))


	def test_False(self):
		for f in (0, 0.0, -0, -0.0, False):
			self.aE(False, objops.ensureBool(f))


	def test_ValueError(self):
		for e in (-0.5, -1.00001, 1.0001, [], {}, set(), float('nan'), float('inf')):
			self.aR(ValueError, lambda: objops.ensureBool(e))
