"""
This module is heavily based on
http://code.activestate.com/recipes/277940-decorator-for-bindingconstants-at-compile-time/
which is Copyright (C) 2004-2010 Raymond Hettinger and licensed under the
PSF License; see LICENSE.txt.
"""

import os
from types import FunctionType, ClassType
from opcode import opmap, HAVE_ARGUMENT, EXTENDED_ARG

# These are known to be present in CPython and pypy 1.4.
STORE_GLOBAL = opmap['STORE_GLOBAL']
LOAD_GLOBAL = opmap['LOAD_GLOBAL']
LOAD_CONST = opmap['LOAD_CONST']
LOAD_ATTR = opmap['LOAD_ATTR']
BUILD_TUPLE = opmap['BUILD_TUPLE']
JUMP_FORWARD = opmap['JUMP_FORWARD']
CALL_FUNCTION = opmap['CALL_FUNCTION']

try:
	# These are known to be present in pypy 1.4.
	LOOKUP_METHOD = opmap['LOOKUP_METHOD']
	CALL_METHOD = opmap['CALL_METHOD']
except KeyError:
	_hasPyPyOpcodes = False
else:
	_hasPyPyOpcodes = True


try:
	_forcePrintDebug = bool(int(
		os.environ['MYPY_REFBINDER_PRINT_DEBUG']))
except (KeyError, ValueError):
	_forcePrintDebug = False


def _debugMessage(logCallable, message):
	if _forcePrintDebug:
		print message

	if logCallable is not None:
		logCallable(message)


_emptySet = set()

def _makeConstants(f, builtinsOnly=False, dontBindNames=_emptySet,
dontBindAttrs=_emptySet, logCallable=None):
	"""
	Return a new function that works like C{f}, but with some
	name/attr/method lookups replaced with constants.

	If a global is known at compile time, replace it with a constant.  Fold
	tuples of constants into a single constant.  Fold constant attribute
	lookups into a single constant.
	"""
	try:
		co = f.func_code
	except AttributeError:
		return f # Jython doesn't have a func_code attribute.
	newcode = map(ord, co.co_code)
	newconsts = list(co.co_consts)
	names = co.co_names
	codelen = len(newcode)

	import __builtin__
	env = vars(__builtin__).copy()
	if builtinsOnly:
		dontBindNames = set(dontBindNames)
		dontBindNames.update(f.func_globals)
	else:
		env.update(f.func_globals)

	# First pass converts global lookups into constants
	i = 0
	while i < codelen:
		opcode = newcode[i]
		if opcode in (EXTENDED_ARG, STORE_GLOBAL):
			return f # for simplicity, only optimize common cases
		if opcode == LOAD_GLOBAL:
			oparg = newcode[i+1] + (newcode[i+2] << 8)
			name = co.co_names[oparg]
			if name in env and name not in dontBindNames:
				value = env[name]
				for pos, v in enumerate(newconsts):
					if v is value:
						break
				else:
					pos = len(newconsts)
					newconsts.append(value)
				newcode[i] = LOAD_CONST
				newcode[i+1] = pos & 0xFF
				newcode[i+2] = pos >> 8
				_debugMessage(logCallable,
					"%s --> %s" % (name, value))
		i += 1
		if opcode >= HAVE_ARGUMENT:
			i += 2

	# Second pass folds tuples of constants and constant attribute lookups
	i = 0
	while i < codelen:

		newtuple = []
		while newcode[i] == LOAD_CONST:
			oparg = newcode[i+1] + (newcode[i+2] << 8)
			newtuple.append(newconsts[oparg])
			i += 3

		opcode = newcode[i]
		if not newtuple:
			i += 1
			if opcode >= HAVE_ARGUMENT:
				i += 2
			continue

		if opcode == LOAD_ATTR:
			obj = newtuple[-1]
			oparg = newcode[i+1] + (newcode[i+2] << 8)
			name = names[oparg]
			if name in dontBindAttrs:
				continue
			try:
				value = getattr(obj, name)
			except AttributeError:
				continue
			deletions = 1

		elif opcode == BUILD_TUPLE:
			oparg = newcode[i+1] + (newcode[i+2] << 8)
			if oparg != len(newtuple):
				continue
			deletions = len(newtuple)
			value = tuple(newtuple)

		else:
			continue

		reljump = deletions * 3
		newcode[i-reljump] = JUMP_FORWARD
		newcode[i-reljump+1] = (reljump-3) & 0xFF
		newcode[i-reljump+2] = (reljump-3) >> 8

		n = len(newconsts)
		newconsts.append(value)
		newcode[i] = LOAD_CONST
		newcode[i+1] = n & 0xFF
		newcode[i+2] = n >> 8
		i += 3
		_debugMessage(logCallable,
			"new folded constant: %r" % (value,))

	codestr = ''.join(map(chr, newcode))
	codeobj = type(co)(
		co.co_argcount, co.co_nlocals, co.co_stacksize, co.co_flags,
		codestr, tuple(newconsts), co.co_names, co.co_varnames,
		co.co_filename, co.co_name, co.co_firstlineno, co.co_lnotab,
		co.co_freevars, co.co_cellvars)
	return type(f)(codeobj, f.func_globals, f.func_name, f.func_defaults,
		f.func_closure)

_makeConstants = _makeConstants(_makeConstants) # optimize thyself!
_debugMessage = _makeConstants(_debugMessage)


# Make sure this function signature matches the one in refbinder.py
def bindRecursive(mc, skip=_emptySet, builtinsOnly=False,
dontBindNames=_emptySet, dontBindAttrs=_emptySet, logCallable=None):
	"""
	Recursively apply constant binding to functions in a module or class,
	skipping functions/classes in C{mc} whose name is in C{skip}.

	Use as the last line of the module (after everything is defined, but
	before test code).  In modules that need modifiable globals, set
	builtinsOnly to True.
	"""
	try:
		d = vars(mc)
	except TypeError:
		return
	for k, v in d.items():
		if k in skip:
			continue
		if type(v) is FunctionType:
			newv = _makeConstants(v, builtinsOnly, dontBindNames,
				dontBindAttrs, logCallable)
			setattr(mc, k, newv)
		elif type(v) in (type, ClassType):
			bindRecursive(v, _emptySet, builtinsOnly, dontBindNames,
				dontBindAttrs, logCallable)


# Make sure this function signature matches the one in refbinder.py
@_makeConstants
def makeConstants(builtinsOnly=False, dontBindNames=_emptySet,
dontBindAttrs=_emptySet, logCallable=None):
	"""
	Return a decorator for optimizing global references.

	Replaces global references with their currently defined values.
	If not defined, the dynamic (runtime) global lookup is left undisturbed.
	If C{builtinsOnly} is True, then only builtins are optimized.
	Variable names in C{dontBindNames} are also left undisturbed.
	Also, folds constant attr lookups and tuples of constants.
	If C{logCallable} is not C{None}, call it with debug messages.

	"""
	if type(builtinsOnly) == type(makeConstants):
		raise ValueError("The makeConstants decorator must have arguments.")
	return lambda f: _makeConstants(f, builtinsOnly, dontBindNames,
		dontBindAttrs, logCallable)
