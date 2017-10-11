# pmb-tools
Set of tools to generate XML files to import in open-source PMB site

1. Import bulletins and articles in XLSX file

How to use :
import sys
from model import Periodique
from xls_to_model import XlsConverter
from model_to_xml import XmlConverter

# Load file
if len(sys.argv) < 2:
	sys.exit("Nom de fichier requis")
filepath = sys.argv[1]
xls = XlsConverter()
try:
	xls.load(filepath)
except Exception as e:
	sys.exit("ERREUR : " + str(e))

# Define periodique
per = Periodique()
per.id = 44
per.name = "Pif Gadget"
xls.setPeriodique(per)

# Parsing
articles = xls.activeSheetToModel()
if len(articles) == 0:
    sys.exit("Aucun article détecté dans le fichier")

xml = XmlConverter()
exportfile = "pif-gadget_" + datetime.datetime.now().strftime("%Y-%b-%d-%I-%M-%S") + ".xml"
xml.loadModelToFile(articles, exportfile)
