"""
Simple image operations that shouldn't require a big library.
"""


import struct


class BadImage(Exception):
	"""Couldn't parse the bytes."""


def readin(stream, length, offset=0):
	if offset != 0:
		stream.seek(offset, 0)
	return stream.read(length)


def png_size(stream):
	"""Return (width, height) of a PNG file object. Also works on MNG."""
	width, height = -1, -1
	if readin(stream, 4, 12) in ('IHDR', 'MHDR'):
		width, height = struct.unpack("!II", stream.read(8))
	return width, height


def gif_size(stream):
	"""
	From http://mail.python.org/pipermail/python-list/2007-June/617126.html
	"""

	# Skip over the identifying string, since we already know this is a GIF
	buf = readin(stream, 5, 6)
	if len(buf) != 5:
		raise BadImage("Invalid/Corrupted GIF (bad header)")
	(sw, sh, x) = struct.unpack("<HHB", buf)
	return (sw, sh)
