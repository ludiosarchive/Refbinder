"""
Random data generator.
"""

import os
import sys

from mypy.objops import ensureNonNegInt

_postImportVars = vars().keys()


class RandomFactory(object):
	"""
	Factory providing a L{secureRandom} method.

	This implementation buffers data from os.urandom,
	to avoid calling it every time random data is needed.

	You should use this instead of L{twisted.python.randbytes}.
	"""
	__slots__ = ('_bufferSize', '_buffer', '_position')

	def __init__(self, bufferSize):
		self._bufferSize = bufferSize
		self._getMore(bufferSize)


	def _getMore(self, howMuch):
		self._buffer = os.urandom(howMuch)
		self._position = 0


	def secureRandom(self, nbytes):
		"""
		Return a number of relatively secure random bytes.

		@param nbytes: number of bytes to generate.
		@type nbytes: C{int}

		@return: a string of random bytes.
		@rtype: C{str}
		"""
		# ugly speed-up for the most common case; feel free to change/remove
		if nbytes is not 16:
			nbytes = ensureNonNegInt(nbytes)

		if nbytes > len(self._buffer) - self._position:
			self._getMore(max(nbytes, self._bufferSize))

		out = self._buffer[self._position:self._position+nbytes]
		self._position += nbytes
		return out



_theRandomFactory = RandomFactory(bufferSize=4096*8)
secureRandom = _theRandomFactory.secureRandom


from mypy import constant_binder
constant_binder.bindRecursive(sys.modules[__name__], _postImportVars)
