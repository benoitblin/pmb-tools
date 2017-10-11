#! /usr/bin/env python3
# coding: utf-8

from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException
from model import Periodique, Bulletin, Article, Author
from factory import AuthorFactory

""" Parse XLS file to build collection of Articles

Restrictions :
- only active sheet is considered
- no headers line
- all Articles are related to the same Periodique
- title of Bulletin can be set on an empty line
- columns should follow dictionnary below

How to use :
conv = XlsConverter()
conv.load("file.xlsx")
conv.setPeriodique(aPeriodiqueObject)
articles = activeSheetToModel()

"""
class XlsConverter():

	# Columns fields definition
	dictionnary = {
	    'bulletin': {
	    	'title': 1, # B
	    	'number': 2, # C
			'period': 3 # D
	    },
	    'article': {
			'author': 0, # A
			'author2': 1, # B
	    	'title': 5, # F
	    	'pagination': 6 # G
	    }
	}

	# Factory to build Author
	authorFctry = AuthorFactory()

	def __init__(self):
		# Periodique related
		self.periodique = Periodique()

	# Load XLS file to read
	def load(self, filepath):
		# Load workbook
		try:
			self.wb = load_workbook(filename=filepath, read_only=True)
		except FileNotFoundError as e:
			raise Exception("Aucun fichier trouvé pour {}".format(filepath))
		except InvalidFileException as e:
			raise Exception("Le fichier {} n'est pas un fichier XLSX valide".format(filepath))

	# Define the Periodique related to this excel sheet
	def setPeriodique(self, periodique):
		self.periodique = periodique

	# Get cell value
	def _getFieldValue(self, row, object, key):
		val = row[self.dictionnary[object][key]].value
		if val is None:
			return ""
		return str(val)

	# Create article from a row
	def _createArticle(self, row):
		article = Article()
		article.title = self._getFieldValue(row, 'article', 'title')
		article.pagination = self._getFieldValue(row, 'article', 'pagination')
		for i in ['author', 'author2']:
			author_fullname = self._getFieldValue(row, 'article', i)
			if author_fullname:
				author = self.authorFctry.fromFullName(author_fullname)
				article.authors.append(author)
		article.periodique = self.periodique
		return article

	# Parse active sheet to create model
	def activeSheetToModel(self):

		ws = self.wb.active
		return self._rowsToModel(ws.rows)

		
	# Iterate on rows to create model
	def _rowsToModel(self, rows):

		title = ""
		oldDate = ""
		articles = []

		for row in rows:

			# Case 1 : Title line of Bulletin
			if row[0].value == "" and self._getFieldValue(row, 'bulletin', 'title') != "":
				# get title and go to next row
				title = self._getFieldValue(row, 'bulletin', 'title')
				continue

			# Case 2 : Detection of new bulletin
			newDate = self._getFieldValue(row, 'bulletin', 'period')
			if oldDate != newDate:
				bulletin = Bulletin()
				bulletin.title = title
				bulletin.number = self._getFieldValue(row, 'bulletin', 'number')
				bulletin.period = newDate
				bulletin.periodique = self.periodique
				# Empty title (in case next bulletin has no title)
				title = ""
				newDate = oldDate

			# Case 3 : Article
			article = self._createArticle(row)
			article.bulletin = bulletin
			articles.append(article)

		return articles

		

