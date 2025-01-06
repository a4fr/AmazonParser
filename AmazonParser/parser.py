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


    def get_element_or_none(self, xpath, regex=None):
        result = self.get_elements_or_none(xpath, max_num_result=1)
        if result:
            if not regex:
                return result[0]
            else:
                res = re.findall(regex, result[0])
                if res:
                    return res[0]
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
                return f"{self.base_url[:-1]}{partial_url}"
            else:
                return f"{self.base_url}{partial_url}"
            

class AmazonAEParser(Parser):
    def get_product_details(self):
        """ Collect Product Details """
        return {
            'title': self.get_title(),
            'brand': self.get_brand_name(),
            'price': self.get_price(),
            'image': self.get_image(),
            'seller_detail': self.get_seller_detail(),
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
    
    def get_image(self):
        """ Extract Image URL """
        landing_img = self.get_element_or_none('//*[@id="landingImage"]/@src')
        original_size_img = self.get_element_or_none('//img[@id="landingImage"]/@data-old-hires')

        if original_size_img:
            return original_size_img
        return landing_img
    
    def get_brand_name(self):
        """ Extract Brand Name """
        text = self.get_element_or_none('//*[@id="bylineInfo"]/text()', r"Visit the (.+) Store")
        if text:
            text = text.strip()
        return text
            
    def get_seller_detail(self):
        """ Extract Seller Details """
        seller_name = self.get_element_or_none('//a[@id="sellerProfileTriggerId"]/text()')
        if seller_name:
            seller_name = seller_name.strip()

        seller_id = self.get_element_or_none('//a[@id="sellerProfileTriggerId"]/@href', r'seller=([\w\d]+)')
        seller_profile_url = f'/sp/?seller={seller_id}'

        return {
            'seller_name': seller_name,
            'seller_profile_url': self.get_full_url(seller_profile_url),
            'seller_id': seller_id,
        }
    