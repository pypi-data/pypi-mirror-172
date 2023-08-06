# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['image_detection_service', 'image_detection_service.api_v1']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0',
 'image-detection-core==0.6.0',
 'image-service-foundation==0.4.0',
 'numpy>=1.16.0,<1.19.0',
 'prometheus-client>=0.6.0',
 'pydantic>=1.7.3,<1.8.0',
 'python-multipart>=0.0.5,<0.0.6',
 'uvicorn>=0.13.3,<0.14.0']

entry_points = \
{'console_scripts': ['image-detection-service_web_start = '
                     'image_detection_service.run:run_cli',
                     'run-cli = image_detection_service.run:run_cli']}

setup_kwargs = {
    'name': 'image-detection-service',
    'version': '0.5.0',
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
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
