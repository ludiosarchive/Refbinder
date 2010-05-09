from twisted.trial import unittest

from mypy import strops


class RreplaceTests(unittest.TestCase):
	"""
	Tests for L{strops.rreplace}
	"""
	def test_rreplace(self):
		self.assertEqual('.pych.pycello.py', strops.rreplace('.pych.pycello.pyc', '.pyc', '.py'))
		self.assertEqual('34', strops.rreplace('33', '3', '4'))
		self.assertEqual('hello', strops.rreplace('hello', 'z', 'x'))



class StringFragmentTests(unittest.TestCase):
	"""
	Tests for L{strops.StringFragment}
	"""
	def test_stringFragmentFull(self):
		f = strops.StringFragment("helloworld", 0, 10)
		self.assertEqual("helloworld", f.toString())
		self.assertEqual("helloworld", str(f.toBuffer()))


	def test_stringFragmentPartial(self):
		f = strops.StringFragment("helloworld", 1, 4)
		self.assertEqual("ello", f.toString())
		self.assertEqual("ello", str(f.toBuffer()))


	def test_repr(self):
		f = strops.StringFragment("helloworld", 1, 4)
		self.assertTrue(repr(f).startswith("<StringFragment for object at 0x"), f)
		self.assertTrue(repr(f).endswith(", pos=1, size=4>"), f)
