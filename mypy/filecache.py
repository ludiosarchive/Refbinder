import os

from mypy.dictops import securedict

_postImportVars = vars().keys()


class _CachedFile(object):
	__slots__ = ('checkedAt', 'fingerprint', 'content')

	def __init__(self, checkedAt, fingerprint, content):
		self.checkedAt = checkedAt
		self.fingerprint = fingerprint
		self.content = content



def defaultFingerprint(filename):
	s = os.stat(filename)
	return s.st_ino, s.st_size, s.st_mtime, s.st_ctime


def defaultGetContent(filename):
	f = open(filename, 'rb')
	try:
		return f.read()
	finally:
		f.close()


class FileCache(object):
	"""
	Generic file cache.  Notes about its behavior:

	-	If it's been more than N seconds since the file was last stat,
		it peforms a stat, and if (mod time, creat time, inode, size) are
		different from last time, re-reads the file.

	-	It never forgets files.

	-	It never automatically updates the cache when you're not
		calling it.
	"""

	__slots__ = ('_getTimeCallable', '_recheckDelay', '_fingerprintCallable',
		'_getContentCallable', '_clearCacheListeners', '_cache')

	def __init__(self, getTimeCallable, recheckDelay,
	fingerprintCallable=defaultFingerprint,
	getContentCallable=defaultGetContent):
		"""
		C{getTimeCallable} is a 0-arg callable that returns the current
			time as a C{float|int|long} in seconds.  This can be any
			clock, as long as it increments by 1 every second.

		C{recheckDelay} is a C{float|int|long}.  If file hasn't been
			stat'ed in this many seconds, it will be stat'ed (at the
			next L{getContent} call).  If == to C{-1}, files are never
			stat'ed or read more than once.

		C{fingerprintCallable} is a callable that takes a filename and
			returns an __eq__able object.

		C{getContentCallable} is a callable that takes a filename and
			returns the content of the file as a C{str}.
		"""
		self._getTimeCallable = getTimeCallable
		self._recheckDelay = recheckDelay
		self._fingerprintCallable = fingerprintCallable
		self._getContentCallable = getContentCallable
		self._clearCacheListeners = []
		self.clearCache()


	def addClearCacheListener(self, callable):
		"""
		Register callable C{callable} to be called every time the cache is
		cleared.

		This is useful if you have "subcaches" that do things like remember
		the md5sum of the file contents.
		"""
		self._clearCacheListeners.append(callable)


	def removeClearCacheListener(self, callable):
		"""
		Unregister callable C{callable}, which will no longer be called
		when the cache is cleared.
		"""
		self._clearCacheListeners.remove(callable)


	def clearCache(self):
		self._cache = securedict()
		# Copy to prevent re-entrancy problems.
		listeners = self._clearCacheListeners[:]
		for callable in listeners:
			callable()


	def getContent(self, filename, transform=None):
		"""
		C{filename} is a C{str} or C{unicode} representing a file name.

		If C{transform} is not C{None}, cache and return
		C{transform(content)} instead of C{content}.  A separate cache
		entry is created for each (transform, filename).

		Returns (content, maybeNew) or raises an exception.
		"""
		cachedFile = self._cache.get((transform, filename))
		if cachedFile:
			if self._recheckDelay == -1:
				return cachedFile.content, False

			timeNow = self._getTimeCallable()
			if cachedFile.checkedAt > timeNow - self._recheckDelay:
				return cachedFile.content, False

			fingerprint = self._fingerprintCallable(filename)
			if fingerprint == cachedFile.fingerprint:
				cachedFile.checkedAt = timeNow
				return cachedFile.content, False
		else:
			timeNow = self._getTimeCallable()
			fingerprint = self._fingerprintCallable(filename)

		content = self._getContentCallable(filename)
		if transform is not None:
			content = transform(content)
		self._cache[(transform, filename)] = _CachedFile(
			timeNow, fingerprint, content)
		return content, True


from pypycpyo import optimizer
optimizer.bind_all_many(vars(), _postImportVars)
