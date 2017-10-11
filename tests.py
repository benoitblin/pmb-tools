from unittest import TestCase
from openpyxl import Workbook
from lxml import etree
from factory import AuthorFactory
from model import Article, Bulletin, Periodique, Author
from xls_to_model import XlsConverter
from model_to_xml import XmlConverter, BlocNode

class AuthorFactoryTestCase(TestCase):

	# Test if author is created from fullname
	def test_author_fullname(self):
		fctry = AuthorFactory()
		aut = fctry.fromFullName("SACQUET Frodo")
		self.assertEqual(aut.last_name, "SACQUET")
		self.assertEqual(aut.first_name, "Frodo")

	# Test if empty author is created from empty fullname
	def test_author_empty(self):
		fctry = AuthorFactory()
		aut = fctry.fromFullName("")
		self.assertEqual(aut.last_name, "")
		self.assertEqual(aut.first_name, "")

class XlsToModelTestCase(TestCase):

	# Test if exception is raised in case of file not found
	def test_load_filenotfound(self):
		xls = XlsConverter()
		with self.assertRaises(Exception):
			xls.load("notfound")

	# Test if exception is raised in case of invalid file
	def test_load_invalidfile(self):
		xls = XlsConverter()
		with self.assertRaises(Exception):
			xls.load('tests.py')

	# Test if articles is created from rows
	def test_rows_to_model(self):
		rows = [
			["", "Titre bulletin"],
			["SACQUET Frodo", "", "125", "janvier 2000", "", "Titre article", "p. 1-10"],
			["Gimli", "Legolas", "125", "janvier 2000", "", "Titre article 2", "p. 11-20"],
			["", "Titre bulletin 2"],
			["LE GRIS Gandalf", "", "126", "juin 2000", "", "Titre article 3", "p. 2-11"],
			["LE GRIS Gandalf", "LE BLANC Saroumane", "126", "juin 2000", "", "Titre article 4", "p. 12-21"],
		]
		wb = Workbook()
		ws = wb.active
		for row in rows:
			ws.append(row)
		xls = XlsConverter()
		articles = xls._rowsToModel(ws.rows)
		self.assertEqual(len(articles), 4)
		self.assertEqual(articles[0].bulletin.title, "Titre bulletin")
		self.assertEqual(articles[0].authors[0].last_name, "SACQUET")
		self.assertEqual(len(articles[0].authors), 1)
		self.assertEqual(articles[1].authors[1].last_name, "")
		self.assertEqual(articles[1].authors[1].first_name, "Legolas")
		self.assertEqual(articles[2].bulletin.number, "126")
		self.assertEqual(articles[2].bulletin.period, "juin 2000")
		self.assertEqual(articles[3].title, "Titre article 4")
		self.assertEqual(articles[3].pagination, "p. 12-21")

class BlocNodeTestCase(TestCase):

	# Test if bloc with fields is created
	def test_with_fields(self):
		node = etree.Element('root')
		bloc = BlocNode("200")
		bloc.addField("a", "Titre")
		bloc.addField("b", "Autre")
		bloc.appendOn(node)
		xml = len(etree.tostring(node))
		xml_proof = len('<root><f c="200"><s c="a">Titre</s><s c="b">Autre</s></f></root>')
		self.assertEqual(xml, xml_proof)

	# Test if bloc with empty field is not created
	def test_with_empty_field(self):
		node = etree.Element('root')
		bloc = BlocNode("200")
		bloc.addField("a", "")
		bloc.appendOn(node)
		xml = len(etree.tostring(node))
		xml_proof = len('<root/>')
		self.assertEqual(xml, xml_proof)


class ModelToXmlTestCase(TestCase):

	# Test if xml is correctly generated
	def test_articles_to_xml(self):
		articles = []
		per = Periodique()
		per.id = 1
		per.name = "Le Seigneur des anneaux"
		bull = Bulletin()
		bull.title = "La communaute de l anneau"
		bull.number = "1"
		bull.period = "1960"
		bull.periodique = per
		article = Article()
		article.title = "Concerning hobbit"
		article.pagination = "p. 1-100"
		article.language = 'fre'
		author = Author()
		author.last_name = 'TOLKIEN'
		author.first_name = 'J.R.R'
		article.authors.append(author)
		article.bulletin = bull
		article.periodique = per
		articles.append(article)
		article = Article()
		article.title = "La comte"
		article.pagination = "p. 101-200"
		article.language = 'fre'
		article.authors.append(author)
		article.bulletin = bull
		article.periodique = per
		articles.append(article)
		conv = XmlConverter()
		flow = conv._toXml(articles)
		xml = len(etree.tostring(flow))
		xml_proof = len('<unimarc><notice><rs>n</rs><dt>a</dt><bl>a</bl><hl>2</hl><el>1</el><rs>i</rs><f c="200"><s c="a">Concerning hobbit</s></f><f c="101"><s c="a">fre</s></f><f c="215"><s c="a">p. 1-100</s></f><f c="700"><s c="a">TOLKIEN</s><s c="b">J.R.R</s><s c="4">070</s></f><f c="461"><s c="t">Le Seigneur des anneaux</s><s c="9">id:1</s><s c="9">lnk:perio</s></f><f c="463"><s c="t">La communaute de l anneau</s><s c="e">1960</s><s c="v">1</s><s c="9">lnk:bull</s></f></notice><notice><rs>n</rs><dt>a</dt><bl>a</bl><hl>2</hl><el>1</el><rs>i</rs><f c="200"><s c="a">La comte</s></f><f c="101"><s c="a">fre</s></f><f c="215"><s c="a">p. 101-200</s></f><f c="700"><s c="a">TOLKIEN</s><s c="b">J.R.R</s><s c="4">070</s></f><f c="461"><s c="t">Le Seigneur des anneaux</s><s c="9">id:1</s><s c="9">lnk:perio</s></f><f c="463"><s c="t">La communaute de l anneau</s><s c="e">1960</s><s c="v">1</s><s c="9">lnk:bull</s></f></notice></unimarc>')
		self.assertEqual(xml, xml_proof)
