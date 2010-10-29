class ReallyEqualMixin(object):

	def assertReallyEqual(self, a, b):
		self.assertTrue(a == b)
		self.assertFalse(a != b)
		self.assertEqual(0, cmp(a, b))


	def assertReallyUnequal(self, a, b):
		self.assertFalse(a == b)
		self.assertTrue(a != b)
		self.assertNotEqual(0, cmp(a, b))
