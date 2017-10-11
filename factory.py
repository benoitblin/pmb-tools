#! /usr/bin/env python3
# coding: utf-8

from model import Author

#Pattern factory for Author class
class AuthorFactory:

	""" Return an Author instance from a string like "LASTNAME Firstname"
	The rule is : a last name is fully uppercased, a first name not
	"""
	def fromFullName(self, fullname):

		author = Author()

		if fullname == "":
			return author

		first_names = []
		last_names = []

		# Split full name by space
		for word in fullname.split(" "):
			# If name is uppercased, it's a lastname
			if(word.isupper()):
				last_names.append(word)
			else:
				first_names.append(word)

		author.first_name = " ".join(first_names)
		author.last_name = " ".join(last_names)

		return author

