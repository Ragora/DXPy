class HTML:
	_text = None
	def __init__(self, text=None):
		self._text = text

	def raw(self, indent=0):
		if (indent < 1):
			return self._text
		else:
			split = self._text.split("\n")
			result = ""
			for element in split:
				line_data = element
				for i in range(indent):
					line_data = "\t" + line_data
				result += line_data + "\n"
			return result

	def html(self, indent=None):
		return self._text

	def __repr__(self):
		return self._text
