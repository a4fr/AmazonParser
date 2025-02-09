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
            

