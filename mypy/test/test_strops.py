import sys
from twisted.trial import unittest

from mypy.testhelpers import ReallyEqualMixin
from mypy import strops


class RreplaceTests(unittest.TestCase):
	"""
	Tests for L{strops.rreplace}
	"""
	def test_rreplace(self):
		self.assertEqual('.pych.pycello.py', strops.rreplace('.pych.pycello.pyc', '.pyc', '.py'))
		self.assertEqual('34', strops.rreplace('33', '3', '4'))
		self.assertEqual('hello', strops.rreplace('hello', 'z', 'x'))



class StringFragmentTests(unittest.TestCase, ReallyEqualMixin):
	"""
	Tests for L{strops.StringFragment}
	"""
	def test_publicAttrs(self):
		f = strops.StringFragment("helloworld", 1, 10)
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
		self.assertReallyEqual(f1, f2)
		self.assertEqual(hash(f1), hash(f2))


	def test_eqSameSlice(self):
		h = "hellohello"
		f1 = strops.StringFragment(h, 0, 5)
		f2 = strops.StringFragment(h, 0, 5)
		self.assertReallyEqual(f1, f2)
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

		self.assertReallyEqual(f1, f2)
		self.assertEqual(hash(f1), hash(f2))


	def test_neqInsideSameString(self):
		h = "hellohello"
		f1 = strops.StringFragment(h, 1, 5)
		f2 = strops.StringFragment(h, 2, 5)
		self.assertReallyNotEqual(f1, f2)


	def test_neqToTuple(self):
		# This test makes assumptions about the internal representation
		# of StringFragment; remember to update this test if it changes.
		h = "hellohello"
		f1 = strops.StringFragment(h, 0, 5)
		self.assertReallyNotEqual(f1, (h, 0, 5))


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



class SlowStringCompareTests(unittest.TestCase):
    """
    Tests for L{strops.slowStringCompare}
    """
    def test_equal(self):
        """
        L{strops.slowStringCompare} returns C{True} for strings that are equal.
        """
        c = strops.slowStringCompare

        self.assertTrue(c('', ''))
        self.assertTrue(c('a', 'a'))
        self.assertTrue(c('ab', 'ab'))
        self.assertTrue(c(
            'abcdefghijklmnopqrstuvwxyz', 'abcdefghijklmnopqrstuvwxyz'))
        self.assertTrue(c('not alphabetical order', 'not alphabetical order'))
        self.assertTrue(c('\x00\xff', '\x00\xff'))

        rainbow = ''.join([chr(x) for x in xrange(256)])
        self.assertTrue(c(rainbow, '' + rainbow))


    def test_notEqual(self):
        """
        L{strops.slowStringCompare} returns C{False} for strings that are not
        equal.
        """
        c = strops.slowStringCompare

        self.assertFalse(c('ab', 'ba'))
        self.assertFalse(c('', '\x00'))
        self.assertFalse(c(' ', '\x00'))
        self.assertFalse(c('\x00\xff', '\x00\xfe'))
        self.assertFalse(c('\xff\x00', '\x00\xfe'))

        rainbow = ''.join([chr(x) for x in xrange(256)])
        self.assertFalse(c(rainbow, rainbow[::-1]))


    def test_unicodeComparison(self):
        """
        If only one argument to L{strops.slowStringCompare} is unicode, the other
        argument will be decoded using the default encoding before comparison
        occurs; if this fails, the comparison will return C{False}.
        Additionally, a C{DeprecationWarning} is raised if either argument is a
        C{unicode} object.
        """
        def _compare(s1, s2):
            if sys.version_info >= (2, 5):
                expected = s1 == s2

                ws = self.flushWarnings(
                    [SlowStringCompareTests.test_unicodeComparison])
                for w in ws:
                    self.assertEquals(w['category'], UnicodeWarning)

                result = strops.slowStringCompare(s1, s2)
            else:
                # When Python 2.4 cannot decode the non-unicode side of a string
                # comparion, it raises UnicodeDecodeError instead of giving a
                # UnicodeWarning and returning False.
                try:
                    expected = s1 == s2
                except UnicodeDecodeError:
                    # Use the exception class itself as a placeholder to represent
                    # the raising of the exception.
                    expected = UnicodeDecodeError

                try:
                    result = strops.slowStringCompare(s1, s2)
                except UnicodeDecodeError:
                    result = UnicodeDecodeError

            self.assertEquals(result, expected)

            [w] = self.flushWarnings(
                [SlowStringCompareTests.test_unicodeComparison])
            self.assertEquals(w['category'], DeprecationWarning)
            self.assertEquals(
                w['message'],
                'Passing unicode strings to slowStringCompare is insecure')

        _compare(u'test', 'test')
        _compare('test', u'test')
        _compare(u'test', u'test')

        _compare(u'\xff', u'\xff')
        _compare('\xff', u'\xff')
        _compare(u'\xff', '\xff')
