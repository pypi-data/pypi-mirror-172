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
['absl-py==1.3.0',
 'easydict==1.10',
 'image-service-foundation==0.4.0',
 'opencv-python>=4.4.0,<5.0.0',
 'pillow==9.2.0',
 'protobuf>=3.20.0,<3.21.0',
 'pytesseract==0.3.10',
 'tensorflow==2.3.0']

setup_kwargs = {
    'name': 'image-detection-core',
    'version': '0.6.0',
    'description': '',
    'long_description': 'None',
    'author': 'Anustup Das',
    'author_email': 'anustup@mediadistillery.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
