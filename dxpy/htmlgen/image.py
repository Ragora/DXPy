"""
"""

from .html import HTML

class Image:
	source = None
	url = None

	def __init__(self, source=None, url=None):
		self.source = source
		self.url = None

	def html(self):
		result = "<img src=\"%s\"></img>" % self.source
		if (self.url is not None):
			result = "<a href=\"%s\">%s</a>" % (self.url, result)
		return result
