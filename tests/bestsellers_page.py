import sys
sys.path.insert(0, '../AmazonParser')
from AmazonParser import *
import glob
from pprint import pprint


html = AmazonAEBestsellersPageParser.get_html_from_file('tests/archives/appliances.html')
p = AmazonAEBestsellersPageParser(html=html, base_url="https://www.amazon.ae/")
pprint(p.get_products())