# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wap', 'wap.commands']

package_data = \
{'': ['*'], 'wap': ['schema/*', 'versions/*']}

install_requires = \
['arrow>=1.2.3,<2.0.0',
 'attrs>=22.1.0,<23.0.0',
 'click>=8.1.3,<9.0.0',
 'httpx>=0.23.0,<0.24.0',
 'jsonschema>=4.15.0,<5.0.0',
 'rich>=12.5.1,<13.0.0',
 'watchfiles>=0.16.1,<0.17.0']

entry_points = \
{'console_scripts': ['wap = wap.__main__:main']}

setup_kwargs = {
    'name': 'wow-addon-packager',
    'version': '0.10.3',
    'description': 'A developer-friendly World of Warcraft addon packager',
    'long_description': '# wap\n\n[![GitHub Actions CI status for default branch](https://github.com/t-mart/wap/actions/workflows/ci.yml/badge.svg)](https://github.com/t-mart/wap/actions/workflows/ci.yml)\n[![Latest release on PyPI](https://img.shields.io/pypi/v/wow-addon-packager)](https://pypi.org/project/wow-addon-packager/)\n\n\n\nA developer-friendly World of Warcraft addon packager.\n\n![demonstration of wap usage](https://raw.githubusercontent.com/t-mart/wap/master/docs/assets/demo.gif)\n\n## Features\n\n- [Builds](https://t-mart.github.io/wap/commands/build/) Retail, Wrath, Classic addons (or all\n  three!)\n- [Publishes](https://t-mart.github.io/wap/commands/publish/) your addons to CurseForge\n- [Generates valid TOC files](https://t-mart.github.io/wap/toc-gen/) automagically\n- [Continuously rebuilds](https://t-mart.github.io/wap/commands/build/#-watch) your addon during\n  development\n- Sets up new addon projects quickly, ready to go with one\n  [command](https://t-mart.github.io/wap/commands/new-project/)\n- Consolidates all configuration in\n  [one easy-to-edit file](https://t-mart.github.io/wap/configuration)\n- Supports and is tested on Windows, macOS, and Linux\n- Has awesome [documentation](https://t-mart.github.io/wap/)\n\n## wap in 5 minutes\n\nThese instructions create and upload a working addon without editing a single line of code!\n\n1. Download and install [Python 3.10](https://www.python.org/downloads/).\n\n2. Install `wap`:\n\n    ```console\n    pip install --upgrade --user wow-addon-packager\n    ```\n\n3. Create a new a project:\n\n    ```console\n    wap new-project\n    ```\n\n    And then, answer the prompts. Don\'t worry too much about your answers -- you can always change\n    them later in your configuration file.\n\n4. Change to your new project\'s directory. For example, if you named it `MyAddon` in the last step,\n   you\'d type:\n\n    ```console\n    cd MyAddon\n    ```\n\n5. Build your addon package and link it to your local World of Warcraft installation:\n\n    ```console\n    wap build --link\n    ```\n\n    At this point, **you can play the game with your addon**.\n\n6. Upload your addon to CurseForge with your\n   [API token](https://authors.curseforge.com/account/api-tokens) so that others can use it:\n\n    ```console\n    wap upload --curseforge-token "<api-token>"\n    ```\n\n## Project Information\n\n- License: MIT\n- PyPI: <https://pypi.org/project/wow-addon-packager/>\n- Source Code: <https://github.com/t-mart/wap>\n- Documentation: <https://t-mart.github.io/wap/>\n- Supported Python Versions: 3.10 and later\n- Badge: [![Packaged by wap](https://img.shields.io/badge/packaged%20by-wap-d33682)](https://github.com/t-mart/wap)\n- Contribution Guide: <https://t-mart.github.io/wap/contributing>\n',
    'author': 'Tim Martin',
    'author_email': 'tim@timmart.in',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/t-mart/wap',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
