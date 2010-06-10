import unittest

from mypy import iterops


class AreAllEqualTests(unittest.TestCase):

	def test_areAllEqual(self):
		self.assertEqual(True, iterops.areAllEqual([1, 1, 1]))
		self.assertEqual(True, iterops.areAllEqual([1, 1.0, True]))
		self.assertEqual(True, iterops.areAllEqual([1]))
		self.assertEqual(True, iterops.areAllEqual([]))
		self.assertEqual(False, iterops.areAllEqual([1, 1, 2]))
		self.assertEqual(False, iterops.areAllEqual([2, 1, 1]))
		self.assertEqual(False, iterops.areAllEqual([object(), object(), object()]))


	def test_areAllEqualGenerators(self):
		"""
		L{iterops.areAllEqual} works on generators as well.
		"""
		self.assertEqual(True, iterops.areAllEqual((x for x in [1, 1, 1])))
		self.assertEqual(False, iterops.areAllEqual((x for x in [1, 2, 3])))
