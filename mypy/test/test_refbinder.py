import random

import sys
from twisted.trial import unittest
from twisted.python import log

# refbinder should be importable on any Python implementation.
# _refbinder might not be, though.
from mypy.refbinder import (bindRecursive, makeConstants, enableBinders,
	areBindersEnabled)

class _BaseExpected(unittest.TestCase):

	def setUp(self):
		enableBinders()
		assert areBindersEnabled()
		self.messages = []


	def _verifyExpected(self, expected=None):
		if expected is None:
			expected = self.expected

		for n, expectedLine in enumerate(expected):
			try:
				line = self.messages[n]
			except IndexError:
				self.fail("line #%d not in messages: %r\nentire stdout:\n%s" % \
					(n, expectedLine, '\n'.join(self.messages)))
			self.assertTrue(
				line.startswith(expectedLine),
				'line %r did not start with %r\nentire stdout:\n%s' % \
					(line, expectedLine, '\n'.join(self.messages)))

		self.assertEqual(len(expected), len(self.messages),
			"had more lines in messages than in expected\nentire stdout:\n%s" % \
				('\n'.join(self.messages),))



class MakeConstantsTests(_BaseExpected):
	builtinsOnly = False
	verbose_mc = True
	dontBindNames = set()

	expected = """\
isinstance --> <built-in function isinstance>
list --> <type 'list'>
tuple --> <type 'tuple'>
str --> <type 'str'>
TypeError --> <type 'exceptions.TypeError'>
type --> <type 'type'>
len --> <built-in function len>
ValueError --> <type 'exceptions.ValueError'>
list --> <type 'list'>
xrange --> <type 'xrange'>
int --> <type 'int'>
random --> <module 'random' from
new folded constant: (<type 'list'>, <type 'tuple'>, <type 'str'>)""".split('\n')

	if sys.subversion[0] == 'PyPy':
		expected.append('new folded constant: <'
			'bound method Random.random of <random.Random object at ')
	else:
		expected.append('new folded constant: <'
			'built-in method random of Random object at ')

	def test_makeConstants(self):
		logCallable = self.messages.append if self.verbose_mc else None
		@makeConstants(logCallable=logCallable,
			builtinsOnly=self.builtinsOnly, dontBindNames=self.dontBindNames)
		def sample(population, k):
			"""
			Choose k unique random elements from a population sequence.
			"""
			if not isinstance(population, (list, tuple, str)):
				raise TypeError('Cannot handle type', type(population))
			n = len(population)
			if not 0 <= k <= n:
				raise ValueError, "sample larger than population"
			result = [None] * k
			pool = list(population)
			for i in xrange(k): # invariant: non-selected at [0,n-i)
				j = int(random.random() * (n-i))
				result[i] = pool[j]
				pool[j] = pool[n-i-1] # move non-selected item into vacancy
			return result

		self._verifyExpected()

		# Run the function with bound names to make sure it still works.
		out = sample(range(100), 30)
		self.assertEqual(30, len(out))



class MakeConstantsWithoutLogCallableTests(MakeConstantsTests):
	"""
	Bind without a logCallable.
	"""
	builtinsOnly = True
	verbose_mc = False

	expected = []



class MakeConstantsBuiltinsOnlyTests(MakeConstantsTests):
	"""
	Bind builtins only.  In this case, 'random' is no longer optimized.
	"""
	builtinsOnly = True
	verbose_mc = True

	expected = """\
isinstance --> <built-in function isinstance>
list --> <type 'list'>
tuple --> <type 'tuple'>
str --> <type 'str'>
TypeError --> <type 'exceptions.TypeError'>
type --> <type 'type'>
len --> <built-in function len>
ValueError --> <type 'exceptions.ValueError'>
list --> <type 'list'>
xrange --> <type 'xrange'>
int --> <type 'int'>
new folded constant: (<type 'list'>, <type 'tuple'>, <type 'str'>)""".split('\n')



class MakeConstantsBuiltinsOnlyPlusDontBindNamesTests(MakeConstantsTests):
	"""
	Bind builtins only with a dontBindNames.
	"""
	builtinsOnly = True
	verbose_mc = True
	dontBindNames = set(['len', 'str'])

	expected = """\
isinstance --> <built-in function isinstance>
list --> <type 'list'>
tuple --> <type 'tuple'>
TypeError --> <type 'exceptions.TypeError'>
type --> <type 'type'>
ValueError --> <type 'exceptions.ValueError'>
list --> <type 'list'>
xrange --> <type 'xrange'>
int --> <type 'int'>""".split('\n')



class _DummyOldStyle:

	def a(self, x):
		pass


	def b(self, x):
		pass



class _DummyNewStyle(object):

	def a(self, x):
		pass


	def b(self, x):
		pass



class BindRecursiveTests(unittest.TestCase):

	def setUp(self):
		enableBinders()
		assert areBindersEnabled()


	def test_bindRecursiveDummyOldStyle(self):
		bindRecursive(_DummyOldStyle)


	def test_bindRecursiveDummyNewStyle(self):
		bindRecursive(_DummyNewStyle)


	def test_bindRecursiveWithSkip(self):
		class BindMe(object):
			def a(self): pass
			def b(self): pass
			def c(self): pass
			def d(self): pass

		old_a = BindMe.a
		old_b = BindMe.b
		old_c = BindMe.c
		old_d = BindMe.d

		bindRecursive(BindMe, skip=['a', 'c'])

		self.assertEqual(BindMe.a, old_a)
		self.assertEqual(BindMe.c, old_c)
		self.assertNotEqual(BindMe.b, old_b)
		self.assertNotEqual(BindMe.d, old_d)
