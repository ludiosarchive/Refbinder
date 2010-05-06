import functools
from collections import deque


class Mailbox(object):
	"""
	A method mailbox, similar to what you'll find in Erlang processes.

	This effectively flattens the call stacks when two objects are
	reentrantly calling each other, and allows you to do something
	when the mailbox is empty (for example, write buffered data to a socket).

	This may be useful if you have an object A which both:
		1) calls something, which in return methods on A
		2) is called without calling anything first

	See Minerva for sample use of this.
	"""
	__slots__ = ('_stoppedSpinningCb', '_spinning', '_pending')

	def __init__(self, stoppedSpinningCb):
		"""
		L{stoppedSpinningCb} is a callable which will be called every time
			Mailbox stops spinning.
		"""
		self._stoppedSpinningCb = stoppedSpinningCb
		self._spinning = False
		self._pending = deque()


	def _spin(self):
		assert not self._spinning, self._spinning
		self._spinning = True
		try:
			while self._pending:
				callable, args, kwargs = self._pending.popleft()
				callable(*args, **kwargs)
		finally:
			self._spinning = False
			# TODO: maybe pass in the error, or a `hadError` boolean?
			self._stoppedSpinningCb()


	def addMail(self, callable, *args, **kwargs):
		self._pending.append((callable, args, kwargs))
		if not self._spinning:
			self._spin()



def mailboxify(mailboxAttr):
	"""
	`mailboxify` a method on a class. L{mailboxAttr} is the attribute
	name for the mailbox to use.

	Sample use:

	class Something(object):
		def __init__(self):
			self._mailbox = Mailbox(self._stoppedSpinning)

		def _stoppedSpinning(self):
			# things to do after all mailbox messages are
			# processed

		@mailboxify('_mailbox')
		def doThing(self):
			# things

		@mailboxify('_mailbox')
		def anotherThing(self):
			# things
	"""
	def wrapper(method):
		@functools.wraps(method)
		def newmethod(self, *args, **kwargs):
			# method is an unbound function here, so prepend self
			args = (self,) + args
			getattr(self, mailboxAttr).addMail(method, *args, **kwargs)
		return newmethod

	return wrapper
