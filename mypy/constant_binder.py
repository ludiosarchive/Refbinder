import os

try:
	_forceOff = bool(int(
		os.environ['MYPY_CONSTANT_BINDER_DISABLE']))
except (KeyError, ValueError):
	_forceOff = False


def _noopBindRecursive(mc, skip=(), builtinsOnly=False,
volatileNames=(), logCallable=None):
	pass


def _noopMakeConstants(builtinsOnly=False, volatileNames=(),
logCallable=None):
	if type(builtinsOnly) == type(_noopMakeConstants):
		raise ValueError("The makeConstants decorator must have arguments.")
	return lambda f: f


def disableBinders():
	"""
	Make L{bindRecursive} and L{makeConstants} essentially do nothing.
	This does not affect already-bound functions.
	"""
	global bindRecursive
	global makeConstants
	bindRecursive = _noopBindRecursive
	makeConstants = _noopMakeConstants


def isNoop():
	return bindRecursive == _noopBindRecursive


if not _forceOff:
	try:
		from mypy import _constant_binder
	except (ImportError, KeyError):
		# ImportError might be raised from a failed opcode.* import.
		# KeyError might be raised from a failed opmap['']
		disableBinders()
	else:
		bindRecursive = _constant_binder.bindRecursive
		makeConstants = _constant_binder.makeConstants
else:
	disableBinders()
