import sys
sys.path.insert(0, '../AmazonParser')
from AmazonParser import *
import glob


if __name__ == '__main__':
    for path in glob.glob('tests/archives/*.html'):
        print('\n',path)
        html = AmazonAEProductPageParser.get_html_from_file(path)
        p = AmazonAEProductPageParser(html=html, base_url="https://www.amazon.ae/") # Create an instance of AmazonAEProductPageParser
        
        print('\nMetadata:')
        for key, value in p.metadata.items():
            print(f'{key}: {value}')
        
        print('\nPage Detail:')
        for key, value in p.get_product_details().items():
            print(f'{key}: {value}')

