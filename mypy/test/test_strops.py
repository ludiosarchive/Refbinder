from twisted.trial import unittest

from mypy import strops


class RreplaceTests(unittest.TestCase):
	def test_rreplace(self):
		self.assertEquals('.pych.pycello.py', strops.rreplace('.pych.pycello.pyc', '.pyc', '.py'))
		self.assertEquals('34', strops.rreplace('33', '3', '4'))
		self.assertEquals('hello', strops.rreplace('hello', 'z', 'x'))
