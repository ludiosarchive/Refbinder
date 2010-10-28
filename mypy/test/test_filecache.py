from twisted.trial import unittest
from twisted.internet.task import Clock

from mypy import filecache


class FileCacheTests(unittest.TestCase):

	def test_fileCache(self):
		clock = Clock()

		def makeFingerprint(filename):
			return (1,)

		count = [0]
		def getContent(filename):
			count[0] += 1
			return filename

		fc = filecache.FileCache(lambda: clock.rightNow, 1.0, makeFingerprint, getContent)
		self.assertEqual('hello world', fc.getContent('hello world'))
		self.assertEqual(1, count[0])
		self.assertEqual('hello world', fc.getContent('hello world'))
		self.assertEqual(1, count[0])
		fc.clearCache()
		self.assertEqual('hello world', fc.getContent('hello world'))
		self.assertEqual(2, count[0])
