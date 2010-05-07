import traceback
from twisted.trial import unittest

from mypy import mailbox
from mypy import iterops


def getStackDepth():
	"""
	Get the current stack depth, excluding this function.
	"""
	return len(traceback.extract_stack()) - 1


class MyError(Exception):
	pass



class MailboxTests(unittest.TestCase):
	"""
	Tests for L{mailbox.Mailbox}.
	"""
	def test_mailbox(self):
		log = []

		def stoppedSpinning(*args, **kwargs):
			log.append(('stoppedSpinning', args, kwargs, getStackDepth()))

		def a(*args, **kwargs):
			log.append(('a', args, kwargs, getStackDepth()))
			m.addMail(b, 3, 4, five=5, six=6)

		def b(*args, **kwargs):
			log.append(('b', args, kwargs, getStackDepth()))

		m = mailbox.Mailbox(stoppedSpinning)
		m.addMail(a)
		# mailbox spins, a is called, b is called, stoppedSpinning is called

		filteredLog = list(entry[0:3] for entry in log) # Don't include stack depths
		self.assertEqual([
			('a', (), {}),
			('b', (3, 4), dict(five=5, six=6)),
			('stoppedSpinning', (), {}),
		], filteredLog)

		stackDepths = list(entry[3] for entry in log)
		if not iterops.areAllEqual(stackDepths):
			self.fail("stack depths should have been all equal, were %r" % (stackDepths,))


	def test_callableRaisesException(self):
		"""
		If a callable raises an exception, the mailbox is emptied,
		the stoppedSpinning callable is called anyway, and then
		the exception is re-raised.
		"""
		log = []

		def stoppedSpinning(*args, **kwargs):
			log.append(('stoppedSpinning', args, kwargs))

		def a(*args, **kwargs):
			log.append(('a', args, kwargs))
			m.addMail(b)
			raise MyError("Just for test_callableRaisesException")

		def b(*args, **kwargs):
			log.append(('b', args, kwargs))

		def c(*args, **kwargs):
			log.append(('c', args, kwargs))

		m = mailbox.Mailbox(stoppedSpinning)
		try:
			m.addMail(a)
		except Exception, e:
			log.append(e.__class__.__name__)

		self.assertEqual([
			('a', (), {}),
			('stoppedSpinning', (), {}),
			'MyError',
		], log)

		# Spin the mailbox again by adding an item; make sure
		# b is not called.

		del log[:]
		m.addMail(c)

		self.assertEqual([
			('c', (), {}),
			('stoppedSpinning', (), {}),
		], log)


	def test_stoppedSpinningCbAddsMail(self):
		"""
		If the stoppedSpinning callback calls addMail, the Mailbox resumes
		spinning, and at the same stack depth.
		"""
		log = []

		count = [0]
		def stoppedSpinning(*args, **kwargs):
			log.append(('stoppedSpinning', args, kwargs, getStackDepth()))
			if count[0] == 0:
				count[0] += 1
				m.addMail(b)

		def a(*args, **kwargs):
			log.append(('a', args, kwargs, getStackDepth()))

		def b(*args, **kwargs):
			log.append(('b', args, kwargs, getStackDepth()))

		m = mailbox.Mailbox(stoppedSpinning)
		m.addMail(a)

		filteredLog = list(entry[0:3] for entry in log) # Don't include stack depths

		self.assertEqual([
			('a', (), {}),
			('stoppedSpinning', (), {}),
			('b', (), {}),
			('stoppedSpinning', (), {}),
		], filteredLog)

		stackDepths = list(entry[3] for entry in log)
		if not iterops.areAllEqual(stackDepths):
			self.fail("stack depths should have been all equal, were %r" % (stackDepths,))


# TODO

#class DemoClass(object):
#	def __init__(self):
#		self.log = []
#
#
#	def func(arg1, arg2):
#		self.log.append((getStackDepth, 'func', arg1, arg2))
#
#
#
