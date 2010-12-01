"""
Simple image operations that shouldn't require a big library.
"""


import struct

_postImportVars = vars().keys()


class BadImage(Exception):
	"""
	Couldn't parse the bytes.
	"""



def _readIn(stream, length, offset=0):
	stream.seek(offset, 0)
	return stream.read(length)


def pngSize(stream):
	"""Return (width, height) of a PNG file object. Also works on MNG."""
	width, height = -1, -1
	if _readIn(stream, 4, 12) in ('IHDR', 'MHDR'):
		width, height = struct.unpack("!II", stream.read(8))
	return width, height


def gifSize(stream):
	"""
	From http://mail.python.org/pipermail/python-list/2007-June/617126.html
	"""
	# Skip over the identifying string, since we already know this is a GIF
	buf = _readIn(stream, 5, 6)
	if len(buf) != 5:
		raise BadImage("Invalid/Corrupted GIF (bad header)")
	sw, sh, x = struct.unpack("<HHB", buf)
	return (sw, sh)


def isPng(s):
	"""
	Returns C{True} if string C{s} starts with a PNG header.
	"""
	if not isinstance(s, str):
		raise TypeError("isPng takes a str, not a %r" % (type(s),))

	return s.startswith('\x89\x50\x4E\x47\x0D\x0A\x1A\x0A')


try:
	from pypycpyo import optimizer
except ImportError:
	pass
else:
	optimizer.bind_all_many(vars(), _postImportVars)
