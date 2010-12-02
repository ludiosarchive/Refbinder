import sys
from twisted.trial import unittest

from mypy import complainer


class ComplainImplicitAsciiConversionsTests(unittest.TestCase):

	def tearDown(self):
		complainer.complainImplicitAsciiConversions(False)


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


	def test_cannotComplain(self):
		was = sys.getdefaultencoding()
		def _resetDefaultEncoding():
			sys.setdefaultencoding(was)
		self.addCleanup(_resetDefaultEncoding)

		reload(sys)
		sys.setdefaultencoding('utf-8')
		self.assertRaises(complainer.CannotComplain,
			lambda: complainer.complainImplicitAsciiConversions(True))
