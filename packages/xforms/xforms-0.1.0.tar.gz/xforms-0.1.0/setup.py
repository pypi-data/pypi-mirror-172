# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xforms']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xforms',
    'version': '0.1.0',
    'description': 'Async HTML forms for Starlette',
    'long_description': '# xforms\n\nAsync HTML forms for Starlette\n\n![PyPI](https://img.shields.io/pypi/v/xforms)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/alex-oleshkevich/xforms/Lint)\n![GitHub](https://img.shields.io/github/license/alex-oleshkevich/xforms)\n![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/xforms)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/xforms)\n![GitHub Release Date](https://img.shields.io/github/release-date/alex-oleshkevich/xforms)\n\n## Installation\n\nInstall `xforms` using PIP or poetry:\n\n```bash\npip install xforms\n# or\npoetry add xforms\n```\n\n## Features\n\n-   TODO\n\n## Quick start\n\nSee example application in [examples/](examples/) directory of this repository.\n',
    'author': 'Alex Oleshkevich',
    'author_email': 'alex.oleshkevich@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alex-oleshkevich/xforms',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10.0,<4.0.0',
}


setup(**setup_kwargs)
