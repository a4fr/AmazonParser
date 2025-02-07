from .parser import Parser
import json

class AmazonAEBestsellersPageParser(Parser):
    def __init__(self, html, base_url=None):
        super().__init__(html, base_url)
        self.is_it_valid_html = self.is_it_valid_html(html)
    
    @staticmethod
    def is_it_valid_html(html):
        # HTML is None
        if html is None:
            return False
        # Not have captcha
        if '<form method="get" action="/errors/validateCaptcha"' in html:
            return False
        return True

    def get_products(self):
        """ Extract all products from the page
            This funstion has limitation of 30 products (because of Amazon's lazy loading)
        """
        products = []
        for product in self.get_elements_or_none('//div[@id="gridItemRoot"]//div[@data-asin!=""]'):
            asin = product.get_element_or_none('./@data-asin')
            title = product.get_element_or_none('.//a[@role="link"]//text()')

            # Bestsellers Rank
            rank = product.get_element_or_none('.//span[contains(text(), "#")]//text()')
            rank = int(rank[1:]) if rank else None

            # Find highest resolution image
            img = product.get_element_or_none('.//img/@src')
            if img and '._AC_UL' in img:
                img = img[:img.find('._AC_UL')] + '.jpg'
            
            # Reviews
            reviews_text = product.get_element_or_none('.//a[contains(@href, "product-review")]/@title')
            if not reviews_text:
                reviews_text = ''
            res = self.extract_with_regex(reviews_text, r'([\d\.]+) out of 5 stars, ([\d]+) ratings')
            if res:
                res = res[0]
                reviews = {
                    'rate': float(res[0]),
                    'coutn': int(res[1]),
                }
            else:
                reviews = None

            # Price
            price = product.get_element_or_none('.//span[contains(@class, "a-color-price")]//text()')
            if price:
                res = self.extract_with_regex(price, r'([\w]+)\s*([\d\.]+)')
                if res:
                    price = {
                        'currency': res[0][0],
                        'amount': float(res[0][1]),
                    }

            product = {
                'asin': asin,
                'bestsellers_rank': rank,
                'img': img,
                'title': title,
                'reviews': reviews,
                'price': price,
            }
            products.append(product)
        return products
    

    def get_asins(self):
        """ Extract all ASINs from the page
            This function doesn't have limitation of 30 products, returns 50 products
        """
        asins = []
        data_client_recs_list = self.get_element_or_none('//div[@class="p13n-desktop-grid"]/@data-client-recs-list')
        if data_client_recs_list:
            data_client_recs_list = json.loads(data_client_recs_list)
            asins = [item['id'] for item in data_client_recs_list]

        return asins
    
    
    def get_nav_tree(self):
        """ Extract all url from Navigation Tree in the left side of page
        """
        links = []
        for a in self.get_elements_or_none('//div[contains(@class, "browse-group")]/../div[2]//a'):
            # URL
            url = self.get_full_url(a.get_element_or_none('./@href'))
            url = url[:url.rfind('/')]

            # Title
            title = a.get_element_or_none('.//text()')
            
            link = {
                'title': title,
                'url': url,
            }
            links.append(link)
        return links