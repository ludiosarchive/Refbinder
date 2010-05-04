from collections import deque


class Mailbox(object):
	"""
	A method mailbox, similar to what you'll find in Erlang processes.

	This may help you improve code where objects are making complicated
	reentrant calls on each other.

	See Minerva for sample use of this.
	"""
	__slots__ = ('object', '_spinning', '_pending')

	def __init__(self, object):
		self.object = object
		self._spinning = False
		self._pending = deque()


	def _spin(self):
		assert not self._spinning, self._spinning
		self._spinning = True
		obj = self.object
		try:
			while self._pending:
				method, args = self._pending.popleft()
				getattr(obj, method)(*args)
		finally:
			self._spinning = False


	def _addMail(self, method, *args):
		self._pending.append((method, args))
		if not self._spinning:
			self._spin()
