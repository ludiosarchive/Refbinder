import sys
from twisted.trial import unittest

from mypy import complainer


class ComplainImplicitAsciiConversionsTests(unittest.TestCase):

	def setUp(self):
		self._wasEncoding = sys.getdefaultencoding()


	def tearDown(self):
		complainer.complainImplicitAsciiConversions(False)

		if self._wasEncoding != sys.getdefaultencoding():
			reload(sys)
			sys.setdefaultencoding(self._wasEncoding)


	def test_enableDisable(self):
		complainer.complainImplicitAsciiConversions(True)

		self.assertWarns(UnicodeWarning,
			"Implicit conversion of str to unicode",
			__file__, lambda: unicode('should-emit-a-warning'))

		complainer.complainImplicitAsciiConversions(False)

		unicode('should-not-emit-a-warning')


	def test_strToUnicode(self):
		complainer.complainImplicitAsciiConversions(True)

		self.assertWarns(UnicodeWarning,
			"Implicit conversion of unicode to str",
			__file__, lambda: str(u'should-emit-a-warning'))


	def test_enableIsIdempotent(self):
		complainer.complainImplicitAsciiConversions(True)
		complainer.complainImplicitAsciiConversions(True)

		self.assertWarns(UnicodeWarning,
			"Implicit conversion of str to unicode",
			__file__, lambda: unicode('should-emit-a-warning'))


	def test_disableIsIdempotent(self):
		complainer.complainImplicitAsciiConversions(True)
		complainer.complainImplicitAsciiConversions(False)
		complainer.complainImplicitAsciiConversions(False)

		unicode('should-not-emit-a-warning')


	def test_cannotComplain(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		self.assertRaises(complainer.CannotComplain,
			lambda: complainer.complainImplicitAsciiConversions(True))


	def test_disableComplaintsWithBadDefaultEncoding(self):
		"""
		Disabling complaints when a bad default encoding is currently set
		effectively does nothing.
		"""
		reload(sys)
		sys.setdefaultencoding('utf-8')
		complainer.complainImplicitAsciiConversions(False)
		complainer.complainImplicitAsciiConversions(False)
