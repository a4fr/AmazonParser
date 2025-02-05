import sys
sys.path.insert(0, '../AmazonParser')
from AmazonParser import *
from pprint import pprint


if __name__ == '__main__':
    html = AmazonAEBestsellersPageParser.get_html_from_file('tests/archives/appliances.html')
    p = AmazonAEBestsellersPageParser(html=html, base_url="https://www.amazon.ae/")
    pprint(p.get_products())
    
    pprint(p.get_nav_tree())