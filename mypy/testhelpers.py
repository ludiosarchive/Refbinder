class ReallyEqualMixin(object):

	def assertReallyEqual(self, a, b):
		self.assertTrue(a == b)
		self.assertFalse(a != b)
		self.assertEqual(0, cmp(a, b))


	def assertReallyUnequal(self, a, b):
		self.assertFalse(a == b)
		self.assertTrue(a != b)
		self.assertNotEqual(0, cmp(a, b))



def todo(reasonOrMethod):
	"""
	This is a both a decorator and a decorator-returner, depending on
	what C{reasonOrMethod} is.

	This allows you to do

	@todo
	def test_that_will_fail(self):
		...

	or

	@todo("some reason or explanation")
	def test_that_will_fail2(self):
		...
	"""

	if hasattr(reasonOrMethod, '__call__'):
		method = reasonOrMethod
		method.todo = 'todo'
		return method

	def decorator(method):
		method.todo = reasonOrMethod
		return method

	return decorator
