from typing import Union
from lxml import etree
import re
from pprint import pprint
from datetime import datetime

class Parser:
    def __init__(self, html: Union[str, etree._Element], base_url=None):
        """ Parser class
            Support html as a text or prtial etree._Element for nested usecase
            BASE_URL uses for create full URL in <a> tags
        """    
        if isinstance(html, str):
            self.html = html
        else:
            self.html = etree.tostring(html, encoding='unicode')
        
        self.base_url = base_url
        self.metadata = self.extract_metadata(self.html)

        # Base URL
        if not self.base_url and 'BASE_URL' in self.metadata:
            self.base_url = self.metadata['BASE_URL']

        if isinstance(html, str):
            self.tree = etree.HTML(html, base_url=self.base_url)
        else:
            self.tree = html

    @staticmethod
    def get_html_from_file(path):
        with open(path, 'r', encoding='utf8') as f:
            file = f.read()
        return file

    @staticmethod
    def extract_metadata(html):
        result = re.findall(r'<!--\s*(\w+)\s*:\s*([^\s]+)\s*-->', html)
        return {item[0].strip(): item[1].strip() for item in result}
    

    @staticmethod
    def extract_with_regex(text, regex: str, pick_one=False):
        """ Find data with regex
            pick_one: return one element or list of found elements

            pick_one=False
            Return: None             -> Nothing found
                    list[srt]        -> r"(\d+)"
                    list[tuple[str]] -> r"(\d+) (\w+)"

            pick_one=True
            Return: None
                    str
                    tuple[str]
        """
        if isinstance(text, Parser):
            text = text.full_text()

        found = re.findall(regex, text)
        if found:
            if pick_one:
                return found[0]
            return found
        return None


    def get_element_or_none(self, *args, **kwargs):
        """ Get Element or None
        """
        result = self.get_elements_or_none(*args, **kwargs, max_num_result=1)
        if result:
            result = result[0]
        return result
    

    def get_elements_or_none(self, xpath:str, regex=None, max_num_result=None):
        """ Get Elements or None
            if regex is provided, it will return the first match

            //text() -> means self.full_text()
            if xpath ended with //text(), it will return the whole text in the element and childrens
                * if you needed just the element text use /text() instead of //text()
        """
        FLAG_FULL_TEXT = False
        if xpath.endswith('//text()'):
            FLAG_FULL_TEXT = True
            xpath = xpath.replace('//text()', '')

        result = self.tree.xpath(xpath)
        if len(result) == 0:
            return None
        
        if max_num_result and len(result) > max_num_result:
            result = result[:max_num_result]
        
        final_result = []
        for r in result:
            # etree._Element
            if isinstance(r, etree._Element):
                r = Parser(html=r, base_url=self.base_url)
                if FLAG_FULL_TEXT:
                    r = r.full_text()
            # str
            else:
                r = r.strip()
            final_result.append(r)

        if regex:
            final_result = [self.extract_with_regex(text=r, regex=regex, pick_one=True) for r in final_result]
        return final_result
    
    def get(self, attribute):
        """ Get Attribute from the class
        """
        return self.get_elements_or_none(f'./@{attribute}')

    def get_full_url(self, partial_url):
        """ Return BASE_URL/PARTIAL_URL """
        if partial_url:
            if self.base_url.endswith('/'):
                return f"{self.base_url[:-1]}{partial_url}"
            else:
                return f"{self.base_url}{partial_url}"
            
    def full_text(self, seperator=' '):
        all_texts = []
        for text in self.tree.itertext():
            text = text.strip()
            if text:
                all_texts.append(text)
        return seperator.join(all_texts)
    
    def __str__(self):
        return self.html
            

class AmazonAEProductPageParser(Parser):
    def get_product_details(self):
        """ Collect Product Details
        """
        return {
            'title': self.get_title(),
            'brand': self.get_brand_name(),
            'price': self.get_price(),
            'stock_availability': self.get_stock_availability(),
            'image': self.get_image(),
            'seller_detail': self.get_seller_detail(),
            'bought_past_mounth': self.get_bought_past_mounth(),
            'customers_reviews': self.get_reviews(),
            'bullet_points': self.get_bullet_points(),
            'date_first_available': self.get_date_first_available(),
            'best_sellers_rank': self.get_best_sellers_rank(),
            'product_bundles': self.get_product_bundles(),
        }
    
    def get_title(self):
        """ Extract Title
        """
        return self.get_element_or_none('//*[@id="productTitle"]/text()')
    
    def get_price(self):
        """ Extract Price and Currency
        """
        res = self.get_element_or_none('//span[@id="tp_price_block_total_price_ww"]//span[@class="a-offscreen"]/text()')
        if res:
            price = float(self.extract_with_regex(res, r'([\d\.]+)', pick_one=True))
            currency = self.extract_with_regex(res, r'([a-zA-Z]+)', pick_one=True).strip()
        
            return {
                    'currency': currency,
                    'value': price,
            }
    
    def get_image(self):
        """ Extract Image URL
        """
        landing_img = self.get_element_or_none('//*[@id="landingImage"]/@src')
        original_size_img = self.get_element_or_none('//img[@id="landingImage"]/@data-old-hires')

        if original_size_img:
            return original_size_img
        return landing_img
    
    def get_brand_name(self):
        """ Extract Brand Name
        """
        text = self.get_element_or_none('//*[@id="bylineInfo"]/text()', r"Visit the (.+) Store")
        if text:
            text = text.strip()
        return text
            
    def get_seller_detail(self):
        """ Extract Seller Details
        """
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
    
    def get_bought_past_mounth(self):
        """ Extract Sales Details
        """
        xpath = '//div[@data-feature-name="socialProofingAsinFaceout"]//span[@class="a-text-bold"]/text()'
        regex = r'([\d\+]+) bought'
        bought_past_mounth = self.get_element_or_none(xpath, regex)
        return bought_past_mounth
    

    def get_bullet_points(self):
        """ Extract Bullet Points
        """
        result = self.get_elements_or_none('//div[@id="feature-bullets"]/ul//li//text()')
        return '\n'.join([item.strip() for item in result])
    
    def get_reviews(self) -> Union[None, dict]:
        """ Extract Reviews
        """
        # Rate
        review_rate = self.get_element_or_none('//span[@id="acrPopover"]/@title', r'([\d\.]+) out of 5 stars')
        if review_rate:
            review_rate = float(review_rate)
        
        # Count
        review_count = self.get_element_or_none('//span[@id="acrCustomerReviewText"]/text()', r'([\d,]+)')
        if review_count:
            review_count = int(review_count.replace(',', ''))

        if review_rate and review_count:
            return {
                'rate': review_rate,
                'count': review_count,
            }
    
    
    def get_date_first_available(self):
        """ Extract 'Date First Available' and return as a Python Date format
        """
        result = self.get_element_or_none('//th[contains(text(), "Date First Available")]/../td/text()')
        if result:
            result = datetime.strptime(result, '%d %B %Y').date()
        return result
    

    def get_best_sellers_rank(self):
        """ Extract Best Sellers Rank
        """
        xpaths = [
            '//th[contains(text(), "Best Sellers Rank")]/../td/span/span',  # Table
            '//span[contains(text(), "Best Sellers Rank")]/../../..//li',   # Bullet Points
        ]
        for xpath in xpaths:
            result = self.get_elements_or_none(xpath)
            if result:
                break

        # No result in all XPaths
        if not result:
            return None
        
        ranks: list[Parser] = []
        for r in result:
            rank = {
                'rank': None,
                'category': None,
                'category_url': None,
            }
            found = r.get_element_or_none('.//text()', regex=r'#([\d]+) in ([\w\s&]+)')
            if found:
                rank['rank'] = int(found[0])
                rank['category'] = ' '.join(self.extract_with_regex(found[1], r'([^\s]+)'))
                
                url = r.get_element_or_none('.//a/@href')
                url = self.get_full_url(partial_url=url)
                rank['category_url'] = url
                ranks.append(rank)
        return ranks
    
    def get_product_bundles(self) -> Union[None, dict]:
        """ Get All bundles of the Product
        """
        bundles = {}
        result: list[Parser] = self.get_elements_or_none('//div[@data-csa-c-content-id="twister"]//li')
        if result:
            for r in result:
                # Title
                # Attempt 1
                title = r.full_text()
                # Attempt 2
                if not title:
                    title = r.get_element_or_none('./@title', r'Click to select (.+)')
                
                # ASIN
                # Attempt 1
                asin = r.get_element_or_none('./@data-csa-c-item-id')
                # Attempt 2
                if not asin:
                    asin = r.get_element_or_none('./@data-dp-url', r'/dp/([\w\d]+)/ref=twister_[\w\d]+')
                    asin = asin.strip() if asin else asin

                if title and asin:
                    bundles[asin] = title
        if bundles:
            return bundles

        
    def get_stock_availability(self):
        """ Return: {"status": False, "quantity": 0}
                    {"status": True, "quantity": (int)}
            
            Quantity: this number in Amazon is at-least quantity.
                      For example in Amazon.ae quantity=30, it means the stock is more than 30
        """
        status = self.get_element_or_none('//*[@id="availability"]//span[contains(@class, "a-color-success")]//text()')
        if status:
            # Out of Stock
            if 'out of stock' in status.lower():
                return {
                    'status': False,
                    'quantity': 0,
                }
            # in Stock
            else:
                quantity = self.get_element_or_none('//select[@name="quantity"]/option[last()]/@value')
                return {
                    'status': True,
                    'quantity': int(quantity),
                }
