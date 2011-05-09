import os

_refbinder = None


def _noopBindRecursive(mc, skip=(), builtinsOnly=False, dontBindNames=(),
dontBindAttrs=(), logCallable=None):
	pass


def _noopMakeConstants(builtinsOnly=False, dontBindNames=(),
dontBindAttrs=(), logCallable=None):
	if type(builtinsOnly) == type(_noopMakeConstants):
		raise ValueError("The makeConstants decorator must have arguments.")
	return lambda f: f


def bindRecursive(*args, **kwargs):
	if _refbinder is None:
		return _noopBindRecursive(*args, **kwargs)
	else:
		return _refbinder.bindRecursive(*args, **kwargs)


def makeConstants(*args, **kwargs):
	if _refbinder is None:
		return _noopMakeConstants(*args, **kwargs)
	else:
		return _refbinder.makeConstants(*args, **kwargs)


def disableBinders():
	"""
	Make L{bindRecursive} and L{makeConstants} essentially do nothing.
	This does not affect already-bound functions.
	"""
	global _refbinder
	_refbinder = None


def enableBinders():
	"""
	Make L{bindRecursive} and L{makeConstants} actually perform constant-
	binding.  This may silently fail, so if you care about whether it worked,
	call L{isEnabled}.
	"""
	global _refbinder
	try:
		from refbinder import _refbinder
	except (ImportError, KeyError, AttributeError):
		# 1) ImportError might be raised from a failed opcode.* import.
		# 2) KeyError might be raised from a failed opmap['']
		# 3) AttributeError might result from a failure in _makeConstants,
		# like what happens in Jython 2.5.2rc2:
		# exceptions.AttributeError: 'tablecode' object has no attribute 'co_consts'
		disableBinders()


def areBindersEnabled():
	return _refbinder is not None


try:
	_autoenable = bool(int(
		os.environ['REFBINDER_AUTOENABLE']))
except (KeyError, ValueError):
	_autoenable = False

if _autoenable:
	enableBinders()
else:
	disableBinders()
