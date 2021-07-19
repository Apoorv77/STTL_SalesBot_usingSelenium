"""
The function check takes 2 arguments: text(string) and keywords_list(list of strings)  
returns True if any of the keywords is found in the text, False otherwise 
"""
import re


def check(text):
    keywords_list = [
        "Software",
        "Application",
        "Product",
        "Bespoke",
        "Customize application",
        "Customize product",
        ".net application",
        "bespoke dot net",
        "custome dot net",
        "enterprise dotnet application",
        "Angular",
        "React",
        "Native",
        "Full Stack",
        "Mobile application",
        "iOS",
        "android",
        "app ",
        "enterprise mobile application",
        "enterpise mobility solution",
        "Magento",
        "Magento solution provider",
        "Ecommerce",
        "Magento multistore",
        "open sourse",
        "php application",
        "drupal",
        "custom cms",
        "joomla",
        "website",
        "web ",
        "SAP Support",
        "SAP B1 Support",
        "SAP Business One Support",
        "SAP B1 Add On",
        "SAP Business One Add On",
        "SAP B1 Implementation",
        "SAP Business One Implementation",
        "RPA Implementation",
        "RPA Consultant",
        "Digitial Transformation Experts",
        "Digital Transformation Consultants",
    ]
    keywords_list = list(map(lambda x: x.lower(), keywords_list))
    text = text.lower()
    words_re = re.compile("|".join(keywords_list))
    if words_re.search(text):
        return True
    return False

