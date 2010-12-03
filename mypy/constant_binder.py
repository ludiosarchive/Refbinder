import os

_constant_binder = None


def _noopBindRecursive(mc, skip=(), builtinsOnly=False,
volatileNames=(), logCallable=None):
	pass


def _noopMakeConstants(builtinsOnly=False, volatileNames=(),
logCallable=None):
	if type(builtinsOnly) == type(_noopMakeConstants):
		raise ValueError("The makeConstants decorator must have arguments.")
	return lambda f: f


def bindRecursive(*args, **kwargs):
	if _constant_binder is None:
		return _noopBindRecursive(*args, **kwargs)
	else:
		return _constant_binder.bindRecursive(*args, **kwargs)


def makeConstants(*args, **kwargs):
	if _constant_binder is None:
		return _noopMakeConstants(*args, **kwargs)
	else:
		return _constant_binder.makeConstants(*args, **kwargs)


def disableBinders():
	"""
	Make L{bindRecursive} and L{makeConstants} essentially do nothing.
	This does not affect already-bound functions.
	"""
	global _constant_binder
	_constant_binder = None


def enableBinders():
	"""
	Make L{bindRecursive} and L{makeConstants} actually perform constant-
	binding.  This may silently fail, so if you care about whether it worked,
	call L{isEnabled}.
	"""
	global _constant_binder
	try:
		from mypy import _constant_binder
	except (ImportError, KeyError):
		# ImportError might be raised from a failed opcode.* import.
		# KeyError might be raised from a failed opmap['']
		disableBinders()


def areBindersEnabled():
	return _constant_binder is not None


try:
	_autoenable = bool(int(
		os.environ['MYPY_CONSTANT_BINDER_AUTOENABLE']))
except (KeyError, ValueError):
	_autoenable = False

if _autoenable:
	enableBinders()
else:
	disableBinders()
