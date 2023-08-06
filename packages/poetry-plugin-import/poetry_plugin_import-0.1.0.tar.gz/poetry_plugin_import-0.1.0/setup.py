# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poetry_plugin_import']

package_data = \
{'': ['*']}

install_requires = \
['poetry-core>=1.3.0,<2.0.0', 'poetry>=1.2.2,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['import = '
                               'poetry_plugin_import.plugins:ImportApplicationPlugin']}

setup_kwargs = {
    'name': 'poetry-plugin-import',
    'version': '0.1.0',
    'description': 'A Poetry plugin that import dependencies from requirements.txt',
    'long_description': '# Poetry Plugin Import\n\nA [Poetry](https://python-poetry.org) plugin that import dependencies from requirements.txt.\n\n## Installation\n\nIn order to install the plugin you need to have installed a poetry version `>1.0` and type:\n\n```bash\npoetry self add poetry-plugin-import\n```\n\n## Usage\n\nImagine the following requirements.txt that you want to import into you pyproject.html\n\n```toml\nasyncio==3.4.3\ngit+https://github.com/neriberto/malwarefeeds.git@0.1.0#egg=malwarefeeds\nrequests==2.22.0\nclick==7.0\n```\n\nthen, to import just run the command below:\n\n```bash\npoetry import\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.',
    'author': 'Neriberto C.Prado',
    'author_email': 'neriberto@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
