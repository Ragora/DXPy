"""
	Simple search-in-file script.

	Copyright (c) 2013 Robert MacGregor
"""
import os
import sys
import os.path

# The number of bytes to read from each file during each file processing iteration
BUFFER_SIZE = 64
# File Extension White List
ALLOWED_EXTENSIONS = [ 'py', 'txt', 'vb', 'cpp', 'c', 'h']
# Print current file being processed?
REPORT_FILE_STATUS = True

def processor(input, directory, files):
	queries, results = input
	for file in files:
		if (directory[len(directory) - 1] != '/'):
			directory += '/'

		abs_path = '%s%s' % (directory, file)
		if (os.path.isdir(abs_path)): continue

		should_skip = True
		for extension in ALLOWED_EXTENSIONS:
			if (abs_path[len(abs_path) - len('.%s' % extension):] in ALLOWED_EXTENSIONS):
				should_skip = False
				break

		if (should_skip): continue
		if (REPORT_FILE_STATUS): 
			print(abs_path)

		with open(abs_path, 'r') as f:	
			good_queries = True
			matched_queries = [ ]
			while (True):
				data = f.read(BUFFER_SIZE)
				if (data == ''): break

				for query in queries:
					query_inclusive, query_data = query

					if (query_data in data and query_inclusive):
						matched_queries.append(query_data)
					elif (query_data in data and not query_inclusive):
						good_queries = False
						break

			if (good_queries is True):
				for query_data in matched_queries:
					if (abs_path not in results.keys()):
						results[abs_path] = ''

					if (query_data not in results[abs_path]):
						results[abs_path] += '"%s", ' % query_data

class Application:
	def main(self):
		if (len(sys.argv) < 3):
			print('Usage: %s <Search Dir> <Search Query> ...' % sys.argv[0])
			return

		queries = [ ]
		for index, argument in enumerate(sys.argv):
			if (index < 2): continue
		
			if (argument[0] == '-'): 
				queries.append((False, argument[1:]))
			else: 
				queries.append((True, argument))

		print('Executing Search------------')
		results = { }
		os.path.walk(sys.argv[1], processor, (queries, results))
		print('Search Complete-------------')
		for key in results.keys():
			matches = results[key]
			print('%s -> %s' % (key, matches.rstrip(', ')))

if __name__ == '__main__': Application().main()
