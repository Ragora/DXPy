"""
	Event chaining system.
"""

import random
import inspect

def default_branch_logic(handle, link, possibilities):
	""" Default branching logic function that is used when None is specified. """
	return random.choice(possibilities)

class Link(object):
	__name__ = "TopLevel"

	dependencies = None
	next_links = None
	previous_link = None
	weight = None
	""" Weight that is used when choosing multiple paths. """

	def __init__(self):
		self.weight = 1
		self.dependencies = { }

		self.previous_links = [ ]
		self.next_links = [ ]

		member_information = inspect.getmembers(self)
		for member_name, member_value in member_information:
			if (type(member_value) is LinkDependency):
				self.dependencies[member_value._name] = member_value._required

	def is_valid(self):
		pass

	def evaluate(self, handle):
		""" Overwritable evaluate method that determines if conditions are met for a given
		link.

		Return false if the storyline cannot go this way.
		Return true otherwise.
		"""
		for dependency_name in self.dependencies.keys():
			if (self.dependencies[dependency_name](handle[dependency_name]) is False):
				return False

		return True

	def append(self, link):
		if (self.next_links is None):
			self.next_links = [ ]

		self.next_links.append(link)
		link.prepend(self)

	def prepend(self, link):
		if (self.previous_links is None):
			self.previous_links = [ ]

		self.previous_link = link

	def execute(self, handle=None, recurse=True, branching=default_branch_logic):
		"""
			fsdfd
		"""
		handle.update()

		possibilities = [ ]
		if (self.next_links is None):
			return

		for link in self.next_links:
			if (link.evaluate(handle) is True):
				possibilities.append(link)

		if (len(possibilities) == 0):
			return

		choice = branching(handle, self, possibilities)
		handle.event_trace.append(choice)
		choice.execute(handle, recurse, branching)

	def export(self, filename):
		with open(filename, "w") as handle:
			for link in self.iterate_forward():
				new_line = ""	
				for current_iteration in range(5):
					new_line += "\t"
				new_line += link.__name__
				handle.write("%s\n" % new_line)

	def count_below(self):
		""" Counts the total number of :class:`Link` instances below this link. """
		result = 0
		for node in self.iterate_forward():
			result += 1

		return result

	def count_above(self):
		""" Counts the total number of :class:`Link` instances above this link. """
		result = 0
		for node in self.iterate_backward():
			result += 1

		return result

	def iterate_forward(self):
		recursive_trace = [ (self, list(self.next_links)) ]
		result_trace = [ ]

		sdfsdfs = [ ]

		total_cloned = 0

		def recurse(current_link):
			#current_depth = len(recursive_trace) - 1
			#current_link, to_iterate = recursive_trace[current_depth]

			#result_trace.append(current_link)

			#yield (current_link, current_depth)
			my_temp = list(current_link.next_links)
			for next_link in current_link.next_links:
				if (next_link in result_trace):
					#print("PISS ON IT")
					sdfsdfs.append(5)
				#	continue

				#recursive_trace.append( (next_link, list(next_link.next_links)) )
				#to_iterate.remove(next_link)

				#for link in recurse(current_trace):
				#	yield link
				my_temp.remove(next_link)
				result_trace.append(next_link)
				recurse(next_link)

				#print("WAT")

				#recursive_trace.pop()

		recurse(self)

		#print("GOT WAT: %u" % len(result_trace))
		#print("TOTAL CLONED: %u" % len(sdfsdfs))
		#for link in recurse(recursive_trace):
		#	yield link
		return result_trace

	def iterate_backward(self):
		recursive_trace = [ self ]

		def recurse(current_trace):
			current_depth = len(recursive_trace) - 1
			current_link = recursive_trace[current_depth]
			yield (current_link, current_depth)

			if (current_link.previous_links is not None):
				for previous_link in current_link.previous_links:
					current_trace.append(previous_link)

					for link in recurse(current_trace):
						yield link

					current_trace.pop()

		for link in recurse(recursive_trace):
			yield link

class Handle(object):
	move_count = None
	event_trace = None

	def __init__(self, copyfrom=None):
		self.move_count = -1
		self.event_trace = [ ]

	def update(self):
		""" Called after a whole simulation 'step'. """
		self.move_count += 1

	def __getitem__(self, key):
		member_information = inspect.getmembers(self)
		for member_name, member_value in member_information:
			if (member_name == key):
				return member_value

	def keys(self):
		return inspect.getmembers(self)

class LinkDependency(object):
	_linkstate = None
	_required = None
	_name = None

	def __init__(self, name, required):
		self._required = required
		self._name = name

	def __cmp__(self, other):
		return self._required == other.value

def random_chain(maximum_depth=4, minimum_depth=2, maximum_branches=2, maximum_links=0, handle_class=Handle, event_chooser=default_branch_logic):
	""" Generates a random chain, attempting to follow the rules specified by each of the children of :class:`Link`.
	If a chain has one or more links that are invalid, they are simply never used when the chain is actually executed.

	Keyword Arguments:
		maximum_depth: The maximum recursion depth that the generator will use. This is effectively the total maximum
	length of your whole chain. The default value for this is 4.
		minimum_depth: The minimum recursion depth that the generator will wait for before allowing a branch to terminate
	prematurely. The default value for this is 2, and is recommended that it has a value of at least 1. A value of zero may
	cause you to get a empty chain returned immediately.
		handle_class: The custom handle class that derives from :class:`Handle` to instantiate during generation. These
	handle instances are used to simulate a sort of program flow that constructs the chain.
	"""

	top_level = Link()

	def recurse(current_trace, information):
		current_handle, current_link, current_event_trace = current_trace[len(current_trace) - 1]

		current_recursive_depth = len(current_event_trace)

		if (current_recursive_depth >= information.maximum_depth or (information.maximum_links > 0 and len(information.link_trace) >= information.maximum_links) or (current_link.next_links is not None and len(current_link.next_links) >= information.maximum_branches)):
			return

		# Collect Possible Event Information
		possible_events = [ ]
		for event_type in Link.__subclasses__():
			event_instance = event_type()
			if (event_instance.evaluate(current_handle)):
				possible_events.append(event_instance)

		if (len(possible_events) == 0):
			return

		# Branch X Times
		minimum_range = 1
		if (current_recursive_depth >= information.minimum_depth):
			minimum_range = 0

		for current_branch_iteration in range(random.randint(minimum_range, information.maximum_branches + 1)):
			if (information.maximum_links > 0 and len(information.link_trace) >= information.maximum_links):
				return

			# Pick an Event
			selected_event = event_chooser(current_handle, current_link, possible_events)
			next_event_trace = list(current_event_trace)
			next_event_trace.append(selected_event)

			next_handle = handle_class(current_handle)
			current_trace.append((next_handle, selected_event, next_event_trace))
			selected_event.execute(handle=next_handle, recurse=False)
			current_link.append(selected_event)

			information.link_trace.append(selected_event)

			recurse(current_trace, information)

			current_trace.pop()

	# Handle at that level, current link, list of events leading up to this,
	recursive_trace_start = (handle_class(), top_level, []) 
	recursive_trace = [ recursive_trace_start ]

	class Information(object):
		maximum_links = 0
		maximum_depth = 0
		minimum_depth = 0
		maximum_branches = 0
		handle_class = 0
		event_chooser = 0

		link_trace = None

	information = Information()
	information.maximum_links = maximum_links
	information.maximum_depth = maximum_depth
	information.minimum_depth = minimum_depth		
	information.maximum_branches = maximum_branches
	information.handle_class = handle_class
	information.event_chooser = event_chooser
	information.link_trace = [ ]

	recurse(recursive_trace, information)

	print("LENGTH: %u" % len(information.link_trace))

	return top_level
