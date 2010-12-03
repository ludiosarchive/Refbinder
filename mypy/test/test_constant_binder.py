import random

import sys
from twisted.trial import unittest
from twisted.python import log

# constant_binder should be importable on any Python implementation.
from mypy.constant_binder import bindAll, makeConstants

hasCPythonBytecode = sys.subversion[0] == 'CPython'

if not hasCPythonBytecode:
	skip = "This Python implementation does not have CPython bytecode."



class _BaseExpected(unittest.TestCase):

	def setUp(self):
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



class MakeConstantsTests(_BaseExpected):
	builtinsOnly = False
	verbose_mc = True
	volatileNames = set()

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
new folded constant: (<type 'list'>, <type 'tuple'>, <type 'str'>)
new folded constant: <built-in method random of Random object at """.split('\n')


	def test_makeConstants(self):
		logCallable = self.messages.append if self.verbose_mc else None
		@makeConstants(logCallable=logCallable,
			builtinsOnly=self.builtinsOnly, volatileNames=self.volatileNames)
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



class MakeConstantsTestsNotVerbose(MakeConstantsTests):
	"""
	Bind without a logCallable.
	"""
	builtinsOnly = True
	verbose_mc = False

	expected = []



class MakeConstantsTestsBuiltinsOnly(MakeConstantsTests):
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



class MakeConstantsTestsBuiltinsOnlyPlusVolatileNames(MakeConstantsTests):
	"""
	Bind builtins only with a volatileNames.
	"""
	builtinsOnly = True
	verbose_mc = True
	volatileNames = set(['len', 'str'])

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



class BindAllTests(unittest.TestCase):

	def test_bind_all_DummyOldStyle(self):
		bindAll(_DummyOldStyle)


	def test_bind_all_DummyNewStyle(self):
		bindAll(_DummyNewStyle)


	def test_bind_all_os(self):
		import os
		bindAll(os)


	def test_bind_all_textwrap(self):
		import textwrap
		bindAll(textwrap)
