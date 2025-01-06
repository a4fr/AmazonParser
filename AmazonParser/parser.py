from lxml import etree
import re
from pprint import pprint

class AmazonParser:
    def __init__(self, html, base_url=None):
        self.base_url = base_url
        self.html = html
        self.metadata = self.extract_metadata(html)

        # Base URL
        if not self.base_url and 'BASE_URL' in self.metadata:
            self.base_url = self.metadata['BASE_URL']
        self.tree = etree.HTML(html, base_url=self.base_url)

    @staticmethod
    def get_html_from_file(path):
        with open(path, 'r', encoding='utf8') as f:
            file = f.read()
        return file

    @staticmethod
    def extract_metadata(html):
        result = re.findall(r'<!--\s*(\w+)\s*:\s*([^\s]+)\s*-->', html)
        return {item[0].strip(): item[1].strip() for item in result}


    def get_element_or_none(self, xpath):
        result = self.tree.xpath(xpath)
        if len(result) == 0:
            return None
        return result[0]


    def get_full_url(self, partial_url):
        """ Return BASE_URL/PARTIAL_URL """
        if partial_url:
            if self.base_url.endswith('/'):
                return f"{self.base_url}{partial_url}"
            else:
                return f"{self.base_url}/{partial_url}"