# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['image_detection_core',
 'image_detection_core.service',
 'image_detection_core.yolo']

package_data = \
{'': ['*']}

install_requires = \
['image-service-foundation==0.1.0']

setup_kwargs = {
    'name': 'image-detection-core',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Anustup Das',
    'author_email': 'anustup@mediadistillery.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
