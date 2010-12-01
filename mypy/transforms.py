"""
Some useful transforms for L{filecache.FileCache}.  It's useful to have them
in one place to prevent duplicated entries in FileCache's content cache.
"""

from hashlib import md5

_postImportVars = vars().keys()


def md5hexdigest(s):
	return md5(s).hexdigest()


try:
	from pypycpyo import optimizer
except ImportError:
	pass
else:
	optimizer.bind_all_many(vars(), _postImportVars)
