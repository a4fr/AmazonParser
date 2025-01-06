import sys
sys.path.insert(0, '../AmazonParser')
from AmazonParser import AmazonParser


if __name__ == '__main__':
    html = AmazonParser.get_html_from_file('tests/archives/B0D83GHDW2.html') # Read HTML file 
    p = AmazonParser(html=html) # Create an instance of AmazonParser
    
    for key, value in p.metadata.items():
        print(f'{key}: {value}')
