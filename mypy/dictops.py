import sys

_postImportVars = vars().keys()


class attrdict(dict):
	"""
	A dict that can be modified by setting and getting attributes.
	This may be broken in funny ways; use with care.
	"""
	__slots__ = ()

	def __setattr__(self, key, value):
		self[key] = value


	def __getattribute__(self, key):
		return self[key]



class consensualfrozendict(dict):
	"""
	A C{dict} that block naive attempts to mutate it, but isn't really
	immutable.

	Allowed to have unhashable values, so it is not necessarily hashable.
	"""
	__slots__ = ('_cachedHash')

	@property
	def _blocked(self):
		raise AttributeError("A consensualfrozendict cannot be modified.")

	__delitem__ = \
	__setitem__ = \
	clear = \
	pop = \
	popitem = \
	setdefault = \
	update = \
	_blocked

	def __new__(cls, *args, **kwargs):
		new = dict.__new__(cls)
		new._cachedHash = None
		dict.__init__(new, *args, **kwargs)
		return new


	# A Python dict can be updated with __init__ after it is created,
	# which is the only reason we override __init__ and __new__.
	def __init__(self, *args, **kwargs):
		pass


	def __hash__(self):
		h = self._cachedHash
		if h is None:
			h = self._cachedHash = hash(tuple(self.iteritems()))
		return h


	def __repr__(self):
		return "consensualfrozendict(%s)" % dict.__repr__(self)



from mypy import refbinder
refbinder.bindRecursive(sys.modules[__name__], _postImportVars)
del refbinder
