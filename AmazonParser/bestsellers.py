from .parser import Parser

class AmazonAEBestsellersPageParser(Parser):
    def get_products(self):
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