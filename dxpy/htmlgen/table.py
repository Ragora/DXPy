from .html import HTML

class Table:
	rows = None
	border = None
	def __init__(self, border=0):
		self.rows = [ ]
		self.border = border

	def html(self):
		data = "<table border=\"%s\">\n" % self.border
		for row in self.rows:
			data += "\t<tr>\n"
			for row_data in row:
				if (type(row_data) is not str):
					data += "\t\t<td>%s</td>\n" % row_data.html()
				else:
					data += "\t\t<td>%s</td>\n" % row_data
			data += "\t</tr>\n"
		data += "</table>"

		result = HTML(text=data)
		return result
