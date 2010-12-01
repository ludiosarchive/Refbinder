class ReallyEqualMixin(object):
	"""
	A mixin for your L{unittest.TestCase}s to better test object equality
	and inequality.  Details at:

	http://ludios.org/ivank/2010/10/testing-your-eq-ne-cmp/
	"""
	def assertReallyEqual(self, a, b):
		# assertEqual first, because it will have a good message if the
		# assertion fails.
		self.assertEqual(a, b)
		self.assertEqual(b, a)
		self.assertTrue(a == b)
		self.assertTrue(b == a)
		self.assertFalse(a != b)
		self.assertFalse(b != a)
		self.assertEqual(0, cmp(a, b))
		self.assertEqual(0, cmp(b, a))


	def assertReallyNotEqual(self, a, b):
		# assertNotEqual first, because it will have a good message if the
		# assertion fails.
		self.assertNotEqual(a, b)
		self.assertNotEqual(b, a)
		self.assertFalse(a == b)
		self.assertFalse(b == a)
		self.assertTrue(a != b)
		self.assertTrue(b != a)
		self.assertNotEqual(0, cmp(a, b))
		self.assertNotEqual(0, cmp(b, a))



def todo(reasonOrMethod):
	"""
	Use this decorator to decorate Twisted trial test methods with a
	C{todo} attribute.

	This allows you to do either

	@todo
	def test_that_will_fail(self):
		...

	or

	@todo("some reason or explanation")
	def test_that_will_fail2(self):
		...

	(This is a both a decorator and a decorator-returner, depending on
	what C{reasonOrMethod} is.)
	"""

	if hasattr(reasonOrMethod, '__call__'):
		method = reasonOrMethod
		method.todo = 'todo'
		return method

	def decorator(method):
		method.todo = reasonOrMethod
		return method

	return decorator
