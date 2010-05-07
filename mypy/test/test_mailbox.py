import traceback
from twisted.trial import unittest

from mypy import mailbox
from mypy import iterops


def getStackDepth():
	"""
	Get the current stack depth, excluding this function.
	"""
	return len(traceback.extract_stack()) - 1


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


	def test_stoppedSpinningAlwaysCalled(self):
		"""
		The stoppedSpinning callback is called even if a callable raised
		an exception.
		"""



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
