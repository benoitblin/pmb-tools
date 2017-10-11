# pmb-tools
Set of tools to generate XML files to import in open-source PMB site

1. Import bulletins and articles from XLSX file
---------------------------------------------

*How to use :*

```python
from model import Periodique
from xls_to_model import XlsConverter
from model_to_xml import XmlConverter

xls = XlsConverter()
try:
	xls.load("source.xlsx")
except Exception as e:
	print("ERREUR : " + str(e))

# Define periodique
per = Periodique()
per.id = 44
per.name = "Pif Gadget"
xls.setPeriodique(per)

# Parsing
articles = xls.activeSheetToModel()

# Produce XML
xml = XmlConverter()
xml.loadModelToFile(articles, "import-pif-gadget.xml")
```
