import sys
sys.path.insert(0, '../AmazonParser')
from AmazonParser import *
from pprint import pprint


if __name__ == '__main__':
    html = AmazonAEBestsellersPageParser.get_html_from_file('tests/archives/appliances.html')
    p = AmazonAEBestsellersPageParser(html=html, base_url="https://www.amazon.ae/")
    pprint(p.get_products())
    print('Len Products:', len(p.get_products()))
    
    pprint(p.get_nav_tree())
    print('len Nav Tree:', len(p.get_nav_tree()))

    print(p.get_asins())
    print('len Asins:', len(p.get_asins()))