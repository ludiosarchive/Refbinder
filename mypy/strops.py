"""
Basic string operations that should have been in Python.
"""

_postImportVars = vars().keys()


def rreplace(string, needle, replacement):
	"""
	If needle in string,
		replace the last instance of L{needle} in L{string} with L{replacement}
	else,
		return the original L{string}
	"""

	location = string.rfind(needle)

	if location == -1:
		return string

	return (string[:location] + replacement + string[location + len(needle):])


from pypycpyo import optimizer
optimizer.bind_all_many(vars(), _postImportVars)
