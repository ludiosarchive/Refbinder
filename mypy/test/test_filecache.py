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
		self.assertEqual(('hello world', True), fc.getContent('hello world'))
		self.assertEqual([1, 1], counts)

		# Advance the clock by less than 1.0s and make sure that not even
		# makeFingerprint is called next time.
		clock.advance(0.1)
		self.assertEqual(('hello world', False), fc.getContent('hello world'))
		self.assertEqual([1, 1], counts)

		# Clear the cache and make sure both makeFingerprint and getContent are called.
		fc.clearCache()
		self.assertEqual(('hello world', True), fc.getContent('hello world'))
		self.assertEqual([2, 2], counts)

		# Advance the clock by 1.0s; make sure makeFingerprint is called
		clock.advance(1.0)
		self.assertEqual(('hello world', False), fc.getContent('hello world'))
		# The fingerprint was the same, so getContent should not have been called.
		self.assertEqual([3, 2], counts)

		# Change the fingerprint, advance the clock by 1.0s; make sure
		# both makeFingerprint and getContent were called.
		fingerprint[0] = ('two',)
		clock.advance(1.0)
		self.assertEqual(('hello world', True), fc.getContent('hello world'))
		# The fingerprint was different, so getContent should have been called.
		self.assertEqual([4, 3], counts)


	def test_withDefaults(self):
		clock = Clock()
		fc = filecache.FileCache(lambda: clock.rightNow, 0.01)
		filename = self.mktemp()
		FilePath(filename).setContent('aaaa')
		self.assertEqual(('aaaa', True), fc.getContent(filename))
		FilePath(filename).setContent('bbbbb')
		self.assertEqual(('aaaa', False), fc.getContent(filename))
		clock.advance(0.01)
		self.assertEqual(('bbbbb', True), fc.getContent(filename))

		# Reading a file that doesn't exist raises an OSError or IOError
		self.assertRaises((OSError, IOError),
			lambda: fc.getContent('does_not_exist'))


	def test_neverRecheck(self):
		clock = Clock()
		fc = filecache.FileCache(lambda: clock.rightNow, -1)
		filename = self.mktemp()
		FilePath(filename).setContent('aaaa')
		self.assertEqual(('aaaa', True), fc.getContent(filename))
		FilePath(filename).setContent('bbbbb')
		clock.advance(3600)
		self.assertEqual(('aaaa', False), fc.getContent(filename))


	def test_transform(self):
		counts = [0]
		def getContent(filename):
			counts[0] += 1
			# Pretend that the content is the filename
			return filename

		clock = Clock()
		fc = filecache.FileCache(lambda: clock.rightNow, -1,
			fingerprintCallable=lambda x: x,
			getContentCallable=getContent)

		self.assertEqual(('aaaa', True), fc.getContent('aaaa'))
		self.assertEqual(1, counts[0])
		self.assertEqual((4, True), fc.getContent('aaaa', transform=len))
		self.assertEqual(2, counts[0])

		# Make sure this doesn't read again
		self.assertEqual((4, False), fc.getContent('aaaa', transform=len))
		self.assertEqual(2, counts[0])


	def test_clearCacheListeners(self):
		clock = Clock()
		fc = filecache.FileCache(lambda: clock.rightNow, -1)
		fc.clearCache()

		def a():
			a.calls += 1
		a.calls = 0

		def b():
			b.calls += 1
		b.calls = 0

		fc.addClearCacheListener(a)
		fc.clearCache()
		self.assertEqual(1, a.calls)

		fc.addClearCacheListener(b)
		fc.clearCache()
		self.assertEqual(2, a.calls)
		self.assertEqual(1, b.calls)

		fc.removeClearCacheListener(a)
		fc.clearCache()
		self.assertEqual(2, a.calls)
		self.assertEqual(2, b.calls)

		fc.removeClearCacheListener(b)
		fc.clearCache()
		self.assertEqual(2, a.calls)
		self.assertEqual(2, b.calls)
