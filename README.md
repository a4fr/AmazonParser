# AmazonParser
Python Library for Parsing Amazon Pages

## Description

AmazonParser is a Python library designed to parse product information from Amazon product pages. It extracts useful data such as product title, price, ratings, and more. It's designed to scrape data mostly by `XPath` and `RegEx`. This design helps to be more modular and configable.

## Prerequisites

- Python 3.6 or higher
- lxml library: `pip install lxml`

## Installation

You can install the library using pip:

```sh
pip install AmazonParser
```

## Usage

Here is an example of how to use the AmazonParser module:

```python
from amazonparser import AmazonParser

# Create an instance of the parser
parser = AmazonParser()

# Parse a product page
path = 'tests/archives/page-ASIN.html'
html = AmazonAEProductPageParser.get_html_from_file(path)
product_data = AmazonAEProductPageParser(html=html, base_url="https://www.amazon.ae/")

# Print the parsed data
print(product_data.get_product_details())
```

### Example Output

The `get_product_details` method returns a dictionary with the following structure:

```python
{'best_sellers_rank': [{'category': 'Mobile Phones & Communication Products',
                        'category_url': 'https://...',
                        'rank': 5},
                       {'category': 'Mobile Phone Screen Protectors',
                        'category_url': 'https://...',
                        'rank': 2}],
 'bought_past_mounth': '500+',
 'brand': 'JETech',
 'bullet_points': 'STRING',
 'customers_reviews': {'count': 21049, 'rate': 4.3},
 'date_first_available': datetime.date(2024, 8, 6),
 'image': 'https://m.media-amazon.com/images/I/71B7WFLtovL._AC_SL1500_.jpg',
 'price': {'currency': 'AED', 'value': 30.99},
 'product_bundles': {'B09BVR4LFY': 'iPhone 13/13 Pro 6.1-Inch',
                     'B09BZ2YD6F': 'iPhone 13 Pro Max 6.7-Inch',
                     'B0B2L6R586': 'iPhone 12/12 Pro 6.1-Inch',
                     'B0B2RQP8MK': 'iPhone 12 Pro Max 6.7-Inch',
                     'B0DBZNC8DL': 'iPhone 16 Pro 6.3-Inch',
                     'B0DBZPXJRH': 'iPhone 16 Pro Max 6.9-Inch',
                     'B0DBZQ2WR3': 'iPhone 16 Plus 6.7-Inch',
                     'B0DBZR3TX7': 'iPhone 16 6.1-Inch'},
 'seller_detail': {'seller_id': 'A11TDSN2MJL3GW',
                   'seller_name': 'JE Products AE',
                   'seller_profile_url': 'https://www.amazon.ae/sp/?seller=A11TDSN2MJL3GW'},
 'stock_availability': {'quantity': 50, 'status': True},
 'title': 'JETech Screen Protector for iPhone 16 Pro Max 6.9-Inch, Tempered '
          'Glass Film with Easy Installation Tool, Case-Friendly, HD Clear, '
          '3-Pack'}
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

