#! /usr/bin/env python3
# coding: utf-8

LANG_FRENCH = 'fre'


class Author:

	def __init__(self):
		self.last_name = ""
		self.first_name = ""


class Periodique:

	def __init__(self):
		self.id = None
		self.name = ""


class Bulletin:

	def __init__(self):
		self.periodique = Periodique()
		self.title = ""
		self.number = ""
		self.period = ""


class Article:

	def __init__(self):
		self.periodique = Periodique()
		self.bulletin = Bulletin()
		self.authors = [] # list of Author
		self.title = ""
		self.pagination = ""
		self.language = LANG_FRENCH