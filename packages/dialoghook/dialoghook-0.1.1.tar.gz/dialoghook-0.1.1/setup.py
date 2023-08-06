# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dialoghook']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'dialoghook',
    'version': '0.1.1',
    'description': '',
    'long_description': 'Dialogflow Request and Response Constructs and validators for Webhooks in Dialogflow ES V2 API\n\nDev Instructions\nRun poetry install to install the env.\nRun poetry run pre-commit install to initialize the git hooks.\nRun poetry run pre-commit run --all-files if there are file that were committed before adding the git hooks.\nActivate the shell with: poetry shell\nLint with: poetry run pylint poetrypackagetemplate/ tests/\nTest with: poetry run pytest --cov=poetrypackagetemplate\n',
    'author': 'aHardReset',
    'author_email': 'ing.aarongaribay@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aHardReset/dialoghook',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
