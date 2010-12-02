"""
Functions to enable complaints about things that Python should complain about.
"""

import sys
import codecs

from mypy.ascii_with_complaints import ENCODING_NAME, getregentry


def _searchFunction(encoding):
	if encoding == ENCODING_NAME:
		return getregentry()


class CannotComplain(Exception):
	pass



def complainImplicitAsciiConversions(complain):
	"""
	If C{complain} is true, emit warnings about implicit unicode<->ascii
	conversions.  If false, disable these warnings.

	If C{sys.getdefaultencoding()} != 'ascii', trying to enable warnings will
	raise L{CannotComplain}.  Notably, PyGTK changes the default encoding to
	'utf-8'; see https://bugzilla.gnome.org/show_bug.cgi?id=132040
	"""
	encodingNow = sys.getdefaultencoding()
	if complain and encodingNow != ENCODING_NAME:
		if encodingNow != "ascii":
			raise CannotComplain(
				"Can only complain if sys.getdefaultencoding() == "
				"'ascii'; was %r" % (encodingNow,))

		if not getattr(sys, 'setdefaultencoding', None):
			reload(sys)

		try:
			codecs.lookup(ENCODING_NAME)
		except LookupError:
			codecs.register(_searchFunction)

		sys.setdefaultencoding(ENCODING_NAME)
	elif not complain and encodingNow == ENCODING_NAME:
		sys.setdefaultencoding('ascii')
