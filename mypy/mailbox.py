"""
You should not use Mailbox because it makes things more confusing.
It looks like it will solve some problem, and it does, but the program
becomes harder to reason about. Instead of using this, just stick to
thinking about all of the possible re-entrancies.

To see a program that used Mailbox, see Minerva's newlink.py
from 2010-05-04 to 2010-06-29. Before and after these dates,
it does not use Mailbox.
"""
import functools
from collections import deque

_postImportVars = vars().keys()


class Mailbox(object):
	"""
	A method mailbox, similar to what you'll find in Erlang processes.

	This effectively flattens the call stacks when two objects are
	reentrantly calling each other, and allows you to do something
	when the mailbox is empty (for example, write buffered data to a socket).

	This may be useful to use on a class A if it has methods which
	calls something, which in return calls methods on A. See Minerva
	for an example of this.
	"""
	__slots__ = ('_stoppedSpinningCb', '_spinning', '_pending', '_noisy')

	def __init__(self, stoppedSpinningCb, noisy=False):
		"""
		L{stoppedSpinningCb} is a callable which will be called every time
			Mailbox stops spinning.
		"""
		self._stoppedSpinningCb = stoppedSpinningCb
		self._spinning = False
		self._pending = deque()
		self._noisy = noisy


	def _spin(self):
		assert not self._spinning, self._spinning
		if self._noisy:
			print "Mailbox: starting spin"
		self._spinning = True
		while self._spinning:
			try:
				while self._pending:
					callable, args, kwargs = self._pending.popleft()
					if self._noisy:
						print "Mailbox: calling", callable, args, kwargs
					callable(*args, **kwargs)
			except:
				self._pending.clear()
				raise
			finally:
				try:
					# TODO: maybe pass in the error, or a `hadError` boolean?
					if self._noisy:
						print "Mailbox: calling", self._stoppedSpinningCb
					self._stoppedSpinningCb()
				finally:
					# Remember, the stoppedSpinning callback may call addMail
					if not self._pending:
						self._spinning = False
		if self._noisy:
			print "Mailbox: ending spin"


	def addMail(self, callable, *args, **kwargs):
		if self._noisy:
			print "Mailbox: addMail", callable, args, kwargs
		self._pending.append((callable, args, kwargs))
		if not self._spinning:
			self._spin()



# In case you have trouble understanding the _spin above, an almost-correct
# version of it looks like this:
#
#	def _spin(self):
#		assert not self._spinning, self._spinning
#		self._spinning = True
#		try:
#			while self._pending:
#				callable, args, kwargs = self._pending.popleft()
#				callable(*args, **kwargs)
#		finally:
#			self._spinning = False
#			self._stoppedSpinningCb()
#
# This simplified version does not properly recover if a callable or if the
# _stoppedSpinningCb raises an exception. Also, if the _stoppedSpinningCb
# calls addMail, this version will increase its stack depth as it spins again.



def mailboxify(mailboxAttr):
	"""
	A decorator to `mailboxify` a method on a class. L{mailboxAttr} is the
	attribute name for the mailbox to use.

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


from pypycpyo import optimizer
optimizer.bind_all_many(vars(), _postImportVars)
