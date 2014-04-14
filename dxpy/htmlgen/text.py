from .html import HTML

class Text:
	text = None
	size = None
	underlined = None
	bold = None
	italic = None
	color = None
	url = None

	def __init__(self, text=None, bold=False, italic=False, underlined=False, color="black", size=3, url=None):
		self.text = str(text)
		self.bold = bold
		self.italic = italic
		self.underlined = underlined
		self.color = color
		self.size = size
		self.url = url

	def html(self, indent=0):
		text = "<font color=\"%s\" size=\"%s\">%s</font>" % (self.color, self.size, self.text)
		if (self.underlined):
			text = "<u>%s</u>" % text
		if (self.bold):
			text = "<b>%s</b>" % text
		if (self.italic):
			text = "<i>%s</i>" % text
		if (self.url is not None):
			text = "<a href=\"%s\">%s</a>" % (self.url, text)
		return HTML(text=text)

	def __repr__(self):
		return self.html()
