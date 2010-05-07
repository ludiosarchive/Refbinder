"""
Operations on iterables.
"""

from mypy import constant

_postImportVars = vars().keys()


PLACEHOLDER = constant.Constant("PLACEHOLDER")


def areAllEqual(iterable):
	"""
	Return C{True} if all items in iterable are equal, else C{False}.
	If no items in iterable, C{True}.

	The implementation does not sort the items. The implementation assumes
	that if every item is equal to last item, they are all transitively equal.
	"""
	last = PLACEHOLDER
	for i in iterable:
		if i != last and last is not PLACEHOLDER:
			return False
		last = i
	return True


from pypycpyo import optimizer
optimizer.bind_all_many(vars(), _postImportVars)
