import unittest
from twisted.python.filepath import FilePath

from mypy import imgops


class ImageSizeTests(unittest.TestCase):
	"""
	Tests for L{imgops.pngSize} and L{imgops.gifSize}
	"""
	images = FilePath(__file__).parent().child('images')
	assert images.isdir(), "%r is not a dir or does not exist" % (images,)

	def test_pngSize(self):
		for dim in [(2901, 1901), (900, 590), (7, 5)]:
			im = self.images.child('%d_%d.png' % dim).open('rb')
			self.assertEqual(dim, imgops.pngSize(im))
			# Do it again.
			self.assertEqual(dim, imgops.pngSize(im))


	def test_gifSize(self):
		for dim in [(2901, 1901), (900, 590), (7, 5)]:
			im = self.images.child('%d_%d.gif' % dim).open('rb')
			self.assertEqual(dim, imgops.gifSize(im))
			# Do it again.
			self.assertEqual(dim, imgops.gifSize(im))


	def test_gifSize_notransparency_interlaced(self):
		for dim in [(2901, 1901), (900, 590), (7, 5)]:
			im = self.images.child('%d_%d_notransparency_interlaced.gif' % dim).open('rb')
			self.assertEqual(dim, imgops.gifSize(im))
			# Do it again.
			self.assertEqual(dim, imgops.gifSize(im))



class IsPngTests(unittest.TestCase):

	def test_isPng(self):
		self.assertTrue(imgops.isPng('\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'))
		self.assertTrue(imgops.isPng('\x89\x50\x4E\x47\x0D\x0A\x1A\x0AX'))
		self.assertFalse(imgops.isPng('\x89\x50\x4E\x47\x0D\x0A\x1A\x0B'))


	def test_isPngTypeError(self):
		self.assertRaises(TypeError, lambda: imgops.isPng(None))
		self.assertRaises(TypeError, lambda: imgops.isPng(1))
		self.assertRaises(TypeError, lambda: imgops.isPng(u'x'))
		self.assertRaises(TypeError, lambda: imgops.isPng(object()))
