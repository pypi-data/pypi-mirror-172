# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['image_service_foundation',
 'image_service_foundation.config',
 'image_service_foundation.storage']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1b3',
 'dropbox==11.35.0',
 'google-cloud-storage>=1.35,<2',
 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'image-service-foundation',
    'version': '0.4.0',
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
