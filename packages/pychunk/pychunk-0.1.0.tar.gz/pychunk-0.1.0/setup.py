# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pychunk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pychunk',
    'version': '0.1.0',
    'description': 'Chunks an iterator',
    'long_description': "# PyChunk\n\nA Python library to chunk list based on number of items or number of chunks\n\n## Why?\n\nPython doesn't come with out of box chunking functionality for lists. Hence I thought of writing a library instead of referring stackoverflow everytime\n\n## Tech Used\n\n1. Peotry for package management\n2. Pytest for testing\n3. Mypy for static code checking\n\n> This is my first time using python types in my project",
    'author': 'Bhavani Ravi',
    'author_email': 'bhavanicodes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
