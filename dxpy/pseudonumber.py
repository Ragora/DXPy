"""
	Pseudo number implementation.

	This software is licensed under the GNU General Public License
	version 3. Please refer to the LICENSE file for more information.
	Copyright (c) 2014 Robert MacGregor
"""

import math

class PseudoNumber:
	""" A pseudo number is just my wording for a number type that is represented
	with an arbitrary number of characters. """
	_value = None
	_digits = None
	_decimal_value = None
	_converted = None

	def __init__(self, digits=None, value=None):
		self._digits = digits
		self._decimal_value = int(value)

		self.convert()

	def convert(self):
		self._value = ''

		if (self._decimal_value == 0):
			self._value = self._digits[0]
			return self._value

		digit_count = len(self._digits) - 1

		start_power = int(math.ceil(self._decimal_value / digit_count))
		temporary = int(self._decimal_value)
		for current_power in reversed(range(start_power + 1)):
			for current_index, current_digit in enumerate(reversed(self._digits)):
				actual_index = digit_count - current_index
				actual_value = actual_index * pow(digit_count + 1, current_power)
				if (actual_value <= temporary and actual_value != 0):
					temporary -= actual_value
					self._value += self._digits[actual_index % (digit_count + 1)]

				if (temporary <= 0):
					for power in range(current_power):
						self._value += self._digits[0]
					return self._value

		return self._value

	def __repr__(self):
		return self.convert()

	def __str__(self):
		return self._value

	def __int__(self):
		return self._decimal_value

	def __add__(self, other):
		return PseudoNumber(self._digits, self._decimal_value + other)

if __name__ == "__main__":
	print("PseudoNumber Example")
	example = PseudoNumber("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 0)
	print(str(example))
