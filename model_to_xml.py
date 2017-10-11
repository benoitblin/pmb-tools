#! /usr/bin/env python3
# coding: utf-8

from lxml import etree

""" Create a new XML node like :
<f c="200">
    <s c="a">Titre</s>
</f>
"""
class BlocNode():
    
    def __init__(self, code):
        # value of "c" attribute
        self.code = code
        # subElements
        self.fields = []
    
    # set subElement values
    def addField(self, code, value = ""):
        # if value is empty, no adding subElement
        if value:
            self.fields.append([code, value])
    
    # generate XML and append it on node
    def appendOn(self, node):

        # if no field has been set, abort
        if len(self.fields) == 0:
            return
        
        f = etree.Element("f", c=self.code);
        for field in self.fields:
            s = etree.Element("s", c=field[0])
            s.text = field[1]
            f.append(s)
        node.append(f)        

""" Convert collection of Article to XML file

How to use :
xml = XmlConverter()
xml.loadModelToFile(aCollectionOfArticle, "file.xml")

"""
class XmlConverter():

    # Convert articles to XML tree and save it on a file
    def loadModelToFile(self, articles, filepath):

        xml = self._toXml(articles)
        with etree.xmlfile(filepath, encoding="utf-8") as xf:
            xf.write(xml)

    # Convert articles to XML tree
    def _toXml(self, articles):

        root = etree.Element("unimarc")

        for article in articles:

            # - Article
            node = self._setArticleHeader()

            # -- Title
            bloc = BlocNode("200")
            bloc.addField("a", article.title)
            bloc.appendOn(node)

            # -- Language
            bloc = BlocNode("101")
            bloc.addField("a", article.language)
            bloc.appendOn(node)

            # -- Pagination
            bloc = BlocNode("215")
            bloc.addField("a", article.pagination)
            bloc.appendOn(node)

            # -- Authors
            for i in range(len(article.authors)):
                code = (i == 0) and "700" or "701"
                bloc = BlocNode(code)
                bloc.addField("a", article.authors[i].last_name)
                bloc.addField("b", article.authors[i].first_name)
                bloc.addField("4", "070")
                bloc.appendOn(node)

            # -- Periodique
            bloc = BlocNode("461")
            bloc.addField("t", article.periodique.name)
            bloc.addField("9", "id:" + str(article.periodique.id))
            bloc.addField("9", "lnk:perio")
            bloc.appendOn(node)

            # -- Bulletin
            bloc = BlocNode("463")
            bloc.addField("e", article.bulletin.period)
            bloc.addField("v", article.bulletin.number)
            bloc.addField("t", article.bulletin.title)
            bloc.addField("9", "lnk:bull")
            bloc.appendOn(node)

            root.append(node)

        return root


    def _setArticleHeader(self):

        node = etree.Element("notice")
        rs = etree.Element("rs")
        rs.text = "n"
        node.append(rs)
        dt = etree.Element("dt")
        dt.text = "a"
        node.append(dt)
        bl = etree.Element("bl")
        bl.text = "a"
        node.append(bl)
        hl = etree.Element("hl")
        hl.text = "2"
        node.append(hl)
        el = etree.Element("el")
        el.text = "1"
        node.append(el)
        ru = etree.Element("rs")
        ru.text = "i"
        node.append(ru)
        
        return node;

