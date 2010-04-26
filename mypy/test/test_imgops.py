from twisted.trial import unittest
from twisted.python.filepath import FilePath

from mypy import imgops


class ImageDimensions(unittest.TestCase):

	def test_png_size(self):
		for dim in [(2901, 1901), (900, 590), (7, 5)]:
			im = FilePath(__file__).parent().child('images').child('%d_%d.png' % dim).open('rb')
			self.assertEquals(dim, imgops.png_size(im))
			# Do it again.
			self.assertEquals(dim, imgops.png_size(im))


	def test_gif_size(self):
		for dim in [(2901, 1901), (900, 590), (7, 5)]:
			im = FilePath(__file__).parent().child('images').child('%d_%d.gif' % dim).open('rb')
			self.assertEquals(dim, imgops.gif_size(im))
			# Do it again.
			self.assertEquals(dim, imgops.gif_size(im))


	def test_gif_size_notransparency_interlaced(self):
		for dim in [(2901, 1901), (900, 590), (7, 5)]:
			im = FilePath(__file__).parent().child('images').child('%d_%d_notransparency_interlaced.gif' % dim).open('rb')
			self.assertEquals(dim, imgops.gif_size(im))
			# Do it again.
			self.assertEquals(dim, imgops.gif_size(im))
