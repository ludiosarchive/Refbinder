import sys
from twisted.trial import unittest

from mypy import complainer


class ComplainImplicitUnicodeConversionsTests(unittest.TestCase):

	def setUp(self):
		self._wasEncoding = sys.getdefaultencoding()


	def tearDown(self):
		complainer.complainImplicitUnicodeConversions(False)

		if self._wasEncoding != sys.getdefaultencoding():
			reload(sys)
			sys.setdefaultencoding(self._wasEncoding)


	def test_enableDisable(self):
		complainer.complainImplicitUnicodeConversions(True)

		self.assertWarns(UnicodeWarning,
			"Implicit conversion of str to unicode",
			__file__, lambda: unicode('should-emit-a-warning'))

		complainer.complainImplicitUnicodeConversions(False)

		unicode('should-not-emit-a-warning')


	def test_strToUnicode(self):
		complainer.complainImplicitUnicodeConversions(True)

		self.assertWarns(UnicodeWarning,
			"Implicit conversion of unicode to str",
			__file__, lambda: str(u'should-emit-a-warning'))


	def test_enableIsIdempotent(self):
		complainer.complainImplicitUnicodeConversions(True)
		complainer.complainImplicitUnicodeConversions(True)

		self.assertWarns(UnicodeWarning,
			"Implicit conversion of str to unicode",
			__file__, lambda: unicode('should-emit-a-warning'))


	def test_disableIsIdempotent(self):
		complainer.complainImplicitUnicodeConversions(True)
		complainer.complainImplicitUnicodeConversions(False)
		complainer.complainImplicitUnicodeConversions(False)

		unicode('should-not-emit-a-warning')


	def test_cannotComplain(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		self.assertRaises(complainer.CannotComplain,
			lambda: complainer.complainImplicitUnicodeConversions(True))


	def test_disableComplaintsWithBadDefaultEncoding(self):
		"""
		Disabling complaints when a bad default encoding is currently set
		effectively does nothing.
		"""
		reload(sys)
		sys.setdefaultencoding('utf-8')
		complainer.complainImplicitUnicodeConversions(False)
		complainer.complainImplicitUnicodeConversions(False)
