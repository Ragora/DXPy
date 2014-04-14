"""
	Page object that contains all known HTML elements and generates
	the HTML data.

	Copyright (c) 2013 Robert MacGregor
"""

from .html import HTML
from .constants import ALIGN_CENTER, ALIGN_NONE

class Page:
	title = None
	elements = None

	_previous_align = ALIGN_NONE

	def __init__(self):
		self.title = "New Page"
		self.elements = [ ]

	def insert(self, element=None):
		self.elements.append(element)

	def export(self, target=None):
		with open(target, "w") as handle:
			handle.write(self.html().raw())

	def set_align(self, alignment=ALIGN_NONE):
		if (alignment == ALIGN_NONE and self._previous_align == ALIGN_CENTER):
			self.elements.append("</center>\n")
		elif (alignment == ALIGN_CENTER):
			self.elements.append("<center>\n")

	def html(self):
		data = "<!-- Generated automatically by HTMLGen Toolkit v0.1.0. Copyright (c) 2013 Robert MacGregor -->\n"
		data += "<HTML>\n"
		data += "\t<head>\n"
		data += "\t\t<title>%s</title>\n" % self.title
		data += "\t</head>\n"

		data += "\t<body>\n"
		for element in self.elements:
			if (type(element) is not str):
				data += element.html().raw(indent=2) + "</br>"
			else:
				data += HTML(text=element + "</br>").raw(indent=2)
		data += "\t</body>\n"

		if (self._previous_align != ALIGN_NONE):
			data += "</center>\n"
		data += "</HTML>"

		return HTML(text=data)
