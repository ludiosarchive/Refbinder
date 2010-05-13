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
	def test_publicAttrs(self):
		f = strops.StringFragment("helloworld", 1, 10)
		self.assertEqual("helloworld", f.string)
		self.assertEqual(1, f.pos)
		self.assertEqual(10, f.size)


	def test_stringFragmentFull(self):
		f = strops.StringFragment("helloworld", 0, 10)
		self.assertEqual("helloworld", str(f))
		self.assertEqual(buffer("helloworld"), f.toBuffer())
		self.assertEqual(10, len(f))


	def test_stringFragmentPartial(self):
		f = strops.StringFragment("helloworld", 1, 4)
		self.assertEqual("ello", str(f))
		self.assertEqual(buffer("ello"), f.toBuffer())
		self.assertEqual(4, len(f))


	def test_repr(self):
		f = strops.StringFragment("helloworld", 1, 4)
		self.assertTrue(repr(f).startswith("<StringFragment for 0x"), repr(f))
		self.assertTrue(repr(f).endswith(", pos=1, size=4, represents 'ello'>"), repr(f))


	def test_eqInsideSameString(self):
		h = "hellohello"
		f1 = strops.StringFragment(h, 0, 5)
		f2 = strops.StringFragment(h, 5, 5)
		self.assertTrue(f1 == f2)
		self.assertFalse(f1 != f2)
		self.assertEqual(hash(f1), hash(f2))


	def test_eqSameSlice(self):
		h = "hellohello"
		f1 = strops.StringFragment(h, 0, 5)
		f2 = strops.StringFragment(h, 0, 5)
		self.assertTrue(f1 == f2)
		self.assertFalse(f1 != f2)
		self.assertEqual(hash(f1), hash(f2))


	def test_differentUnderlyingStringsSameHash(self):
		"""
		hash()es to the same hash even if the underlying string
		objects are not the same object.
		"""
		s1 = "x" * 1024
		s2 = "x" * 1024
		f1 = strops.StringFragment(s1, 0, 5)
		f2 = strops.StringFragment(s2, 0, 5)

		self.assertTrue(f1 == f2)
		self.assertFalse(f1 != f2)
		self.assertEqual(hash(f1), hash(f2))


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


	def test_getItem(self):
		f1 = strops.StringFragment("helloworld", 1, 5)
		self.assertEqual("e", f1[0])
		self.assertEqual("o", f1[3])
		self.assertEqual("w", f1[-1])
		self.assertEqual("o", f1[-2])
		self.assertEqual("e", f1[-5])

		self.assertRaises(IndexError, lambda: f1[5])
		self.assertRaises(IndexError, lambda: f1[-6])


	def test_getItemForShortFragment(self):
		f1 = strops.StringFragment("helloworld", 9, 1)
		self.assertEqual("d", f1[0])
		self.assertEqual("d", f1[-1])

		self.assertRaises(IndexError, lambda: f1[1])
		self.assertRaises(IndexError, lambda: f1[-2])


	def test_slice(self):
		f1 = strops.StringFragment("helloworld", 0, 5)
		self.assertEqual("ello", str(f1[1:5]))
		self.assertEqual(4, len(f1[1:5]))


	def test_sliceToEmpty(self):
		f1 = strops.StringFragment("helloworld", 0, 5)
		self.assertEqual("", str(f1[5:1000]))
		self.assertEqual(0, len(f1[5:1000]))


	def test_sliceTooFar(self):
		f1 = strops.StringFragment("helloworld", 0, 5)
		self.assertEqual("", str(f1[100:1000]))
		self.assertEqual(0, len(f1[100:1000]))


	def test_sliceNoEnd(self):
		f1 = strops.StringFragment("helloworld", 0, 5)
		self.assertEqual("ello", str(f1[1:]))
		self.assertEqual(4, len(f1[1:]))


	def test_sliceNoBeginning(self):
		f1 = strops.StringFragment("helloworld", 1, 6)
		self.assertEqual("ello", str(f1[:4]))
		self.assertEqual(4, len(f1[:4]))


	def test_sliceTheEnd(self):
		f1 = strops.StringFragment("helloworld", 0, 5)
		self.assertEqual("lo", str(f1[-2:]))
		self.assertEqual(2, len(f1[-2:]))
