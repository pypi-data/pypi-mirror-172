# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openapi_readme']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['openapi-readme = openapi_readme.main:app']}

setup_kwargs = {
    'name': 'openapi-readme',
    'version': '0.1.1',
    'description': 'Generate Markdown from an openapi JSON file.',
    'long_description': '# OpenAPI Readme Generator\n\nGenerates Markdown suitable for a README file from a local `openapi.json` file.\n\n## Usage\n\nRun this in the same directory as your `openapi.json` file. By default the\nMarkdown output will be printed to the console, but you can redirect it out to\na file too.\n\nThe particular styling of the generated Markdown is currently hardcoded, though\nplans are afoot to implement some sort of themeing.\n\n## Options\n\n### --help\n\nShow application usage hints and help.\n\n### --route-level\n\nSpecify the heading level for each Route in the generated documentation. This\ndefaults to **4** if not specified, ie:\n\n```Markdown\n#### **`GET`** _/user/list_\n```\n\n### --inject\n\nInjects the new Markdown directly into a `README.md` file in the current\ndirectory, if it is found.\nYou need to add the placeholder comment `<!--\nopenapi-schema -->` to your markdown where you want it to be injected:\n\n```Markdown\nThis is some preceeding text\n\n### API Schema description\n<!-- openapi-schema -->\n\n### Next section\nThe document continues unaffected after the injection.\n```\n\n<!-- openapi-schema -->\n',
    'author': 'Grant Ramsay',
    'author_email': 'grant@gnramsay.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/seapagan/openapi-readme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
