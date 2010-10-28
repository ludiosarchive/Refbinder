from twisted.trial import unittest
from twisted.internet.task import Clock
from twisted.python.filepath import FilePath

from mypy import filecache


class FileCacheTests(unittest.TestCase):

	def test_functionality(self):
		clock = Clock()

		fingerprint = [('one',)]

		counts = [0, 0]
		def makeFingerprint(filename):
			counts[0] += 1
			return fingerprint[0]

		def getContent(filename):
			counts[1] += 1
			# Pretend that the content is the filename
			return filename

		fc = filecache.FileCache(lambda: clock.rightNow, 1.0, makeFingerprint, getContent)
		self.assertEqual('hello world', fc.getContent('hello world'))
		self.assertEqual([1, 1], counts)

		# Advance the clock by less than 1.0s and make sure that not even
		# makeFingerprint is called next time.
		clock.advance(0.1)
		self.assertEqual('hello world', fc.getContent('hello world'))
		self.assertEqual([1, 1], counts)

		# Clear the cache and make sure both makeFingerprint and getContent are called.
		fc.clearCache()
		self.assertEqual('hello world', fc.getContent('hello world'))
		self.assertEqual([2, 2], counts)

		# Advance the clock by 1.0s; make sure makeFingerprint is called
		clock.advance(1.0)
		self.assertEqual('hello world', fc.getContent('hello world'))
		# The fingerprint was the same, so getContent should not have been called.
		self.assertEqual([3, 2], counts)

		# Change the fingerprint, advance the clock by 1.0s; make sure
		# both makeFingerprint and getContent were called.
		fingerprint[0] = ('two',)
		clock.advance(1.0)
		self.assertEqual('hello world', fc.getContent('hello world'))
		# The fingerprint was different, so getContent should have been called.
		self.assertEqual([4, 3], counts)


	def test_withDefaults(self):
		clock = Clock()
		fc = filecache.FileCache(lambda: clock.rightNow, 0.01)
		filename = self.mktemp()
		FilePath(filename).setContent('aaaa')
		self.assertEqual('aaaa', fc.getContent(filename))
		FilePath(filename).setContent('bbbbb')
		self.assertEqual('aaaa', fc.getContent(filename))
		clock.advance(0.01)
		self.assertEqual('bbbbb', fc.getContent(filename))

		# Reading a file that doesn't exist raises an OSError or IOError
		self.assertRaises((OSError, IOError),
			lambda: fc.getContent('does_not_exist'))


	def test_neverRecheck(self):
		clock = Clock()
		fc = filecache.FileCache(lambda: clock.rightNow, -1)
		filename = self.mktemp()
		FilePath(filename).setContent('aaaa')
		self.assertEqual('aaaa', fc.getContent(filename))
		FilePath(filename).setContent('bbbbb')
		clock.advance(3600)
		self.assertEqual('aaaa', fc.getContent(filename))
