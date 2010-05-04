import traceback
from twisted.trial import unittest

from mypy import mailbox


def getStackDepth():
	"""
	Get the current stack depth, excluding this function.
	"""
	return len(traceback.extract_stack()) - 1


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
#class MailboxTests(unittest.TestCase):
#	def test_mailbox(self):
#		demo = DemoClass()
#		m = mailbox.Mailbox(demo)
