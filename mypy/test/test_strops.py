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
		self.assertEqual(10, len(f))


	def test_stringFragmentPartial(self):
		f = strops.StringFragment("helloworld", 1, 4)
		self.assertEqual("ello", f.toString())
		self.assertEqual("ello", str(f.toBuffer()))
		self.assertEqual(4, len(f))


	def test_repr(self):
		f = strops.StringFragment("helloworld", 1, 4)
		self.assertTrue(repr(f).startswith("<StringFragment for object at 0x"), f)
		self.assertTrue(repr(f).endswith(", pos=1, size=4>"), f)


	def test_eqInsideSameString(self):
		h = "hellohello"
		f1 = strops.StringFragment(h, 0, 5)
		f2 = strops.StringFragment(h, 5, 5)
		self.assertTrue(f1 == f2)
		self.assertFalse(f1 != f2)


	def test_eqSameSlice(self):
		h = "hellohello"
		f1 = strops.StringFragment(h, 0, 5)
		f2 = strops.StringFragment(h, 0, 5)
		self.assertTrue(f1 == f2)
		self.assertFalse(f1 != f2)


	def test_neqInsideSameString(self):
		h = "hellohello"
		f1 = strops.StringFragment(h, 1, 5)
		f2 = strops.StringFragment(h, 2, 5)
		self.assertFalse(f1 == f2)
		self.assertTrue(f1 != f2)


	def test_neqToTuple(self):
		# This test makes assumptions about the internal representation
		# of StringFragment; remember to update this test if it changes.
		h = "hellohello"
		f1 = strops.StringFragment(h, 0, 5)
		self.assertFalse(f1 == (h, 0, 5))
		self.assertTrue(f1 != (h, 0, 5))


	def test_slice(self):
		f1 = strops.StringFragment("helloworld", 0, 5)
		self.assertEqual("ello", f1[1:5].toString())
		self.assertEqual(4, len(f1[1:5]))


	def test_sliceToEmpty(self):
		f1 = strops.StringFragment("helloworld", 0, 5)
		self.assertEqual("", f1[5:1000].toString())
		self.assertEqual(0, len(f1[5:1000]))


	def test_sliceTooFar(self):
		f1 = strops.StringFragment("helloworld", 0, 5)
		self.assertEqual("", f1[100:1000].toString())
		self.assertEqual(0, len(f1[100:1000]))


	def test_sliceNoEnd(self):
		f1 = strops.StringFragment("helloworld", 0, 5)
		self.assertEqual("ello", f1[1:].toString())
		self.assertEqual(4, len(f1[1:]))


	def test_sliceNoBeginning(self):
		f1 = strops.StringFragment("helloworld", 0, 5)
		self.assertEqual("hell", f1[:4].toString())
		self.assertEqual(4, len(f1[:4]))


	def test_sliceTheEnd(self):
		f1 = strops.StringFragment("helloworld", 0, 5)
		self.assertEqual("lo", f1[-2:].toString())
		self.assertEqual(2, len(f1[-2:]))
