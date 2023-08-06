# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['converter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ssi-converter-thuongnn',
    'version': '0.1.0',
    'description': 'demo',
    'long_description': '# Converter\n\nConvert XML to JSON\n\n\n### prerequisite\n- you need to install below library using pip\n- $ pip install xmltodict\n \n### Description\n- It coverts any input.xml file into output.json.\n\n### How to run the script\n\n- First rename your file to input.xml \n- Execute `python3 converter.py`\n- The Output will be shown below as output.json\n\n## *Author Name*\nAzhad Ghufran\n\n\n# Testing',
    'author': 'Nguyen Nhu Thuong',
    'author_email': 'thuongnn6666@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
