from lxml import etree
import re
from pprint import pprint

class Parser:
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
        result = self.get_elements_or_none(xpath, max_num_result=1)
        if result:
            return result[0]
        return None
    

    def get_elements_or_none(self, xpath, max_num_result=None):
        result = self.tree.xpath(xpath)
        if len(result) == 0:
            return None
        
        max_num_result = max_num_result if max_num_result > 0 else None
        if max_num_result and len(result) > max_num_result:
            return result[:max_num_result]
        return result


    def get_full_url(self, partial_url):
        """ Return BASE_URL/PARTIAL_URL """
        if partial_url:
            if self.base_url.endswith('/'):
                return f"{self.base_url}{partial_url}"
            else:
                return f"{self.base_url}/{partial_url}"
            

class AmazonAEParser(Parser):
    def get_product_details(self):
        """ Collect Product Details """
        return {
            'title': self.get_title(),
            'price': self.get_price(),
        }
    
    def get_title(self):
        """ Extract Title """
        return self.get_element_or_none('//*[@id="productTitle"]/text()').strip()
    
    def get_price(self):
        """ Extract Price and Currency """
        res = self.get_element_or_none('//span[@id="tp_price_block_total_price_ww"]//span[@class="a-offscreen"]/text()')
        if res:
            res = res.strip()
            price = float(res.split(' ')[1])
            currency = res.split(' ')[0].strip()
        
        return {
                'currency': currency,
                'value': price,
        }
    