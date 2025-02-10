import sys
sys.path.insert(0, '../AmazonParser')
from AmazonParser import *
import glob
from pprint import pprint


if __name__ == '__main__':
    for path in glob.glob('tests/archives/B00LAYVPOU.html'):
        print('\n',path)
        html = AmazonAEProductPageParser.get_html_from_file(path)

        print('Is Valid HTML:', AmazonAEProductPageParser.is_it_valid_html(html))
        p = AmazonAEProductPageParser(html=html, base_url="https://www.amazon.ae/") # Create an instance of AmazonAEProductPageParser
        
        print('\nMetadata:')
        for key, value in p.metadata.items():
            print(f'{key}: {value}')
        
        print('\nPage Detail:')
        pprint(p.get_product_details())

