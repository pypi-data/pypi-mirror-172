# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moss',
 'moss.ems',
 'moss.ems.extra',
 'moss.ems.scripts',
 'moss.ems.scripts.utilities',
 'moss.ems.utilities']

package_data = \
{'': ['*']}

install_requires = \
['anytree>=2.8.0,<3.0.0', 'requests>=2.28.0,<3.0.0', 'tqdm>=4.64.0,<5.0.0']

scripts = \
['moss\\ems\\scripts\\moss_emscli.py']

setup_kwargs = {
    'name': 'moss-emspy',
    'version': '2.0.11',
    'description': 'Package to interact with MOSS WEGA-EMS',
    'long_description': '# MOSS emspy\n\n## Description\n\nThis is the Python SDK to interact with [M.O.S.S. Computer Grafik Systeme GmbH](https://www.moss.de/wega/) WEGA-EMS\n\n## Installation\n\nThis package kann be installed using pip\n\n```shell\npython -m pip install moss_emspy\n```\n\n## Usage\n\n```python\nmy_service = Service("http://localhost:8080/wega-ems/",\n            username="Test",\n            password="Test")\nmy_service.projects\n```\n',
    'author': 'M.O.S.S.Computer Grafik Systeme GmbH',
    'author_email': 'develop@moss.de',
    'maintainer': 'M.O.S.S.Computer Grafik Systeme GmbH',
    'maintainer_email': 'develop@moss.de',
    'url': 'https://www.moss.de/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'scripts': scripts,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
