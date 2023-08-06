# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cairo_toolkit', 'src', 'src.cairo_toolkit']

package_data = \
{'': ['*']}

install_requires = \
['cairo-lang>=0.10.0,<0.11.0', 'click==8.1.3', 'toml==0.10.2']

entry_points = \
{'console_scripts': ['cairo-toolkit = src.cli:main']}

setup_kwargs = {
    'name': 'cairo-toolkit',
    'version': '1.0.0',
    'description': 'A set of useful tools for cairo / starknet development.',
    'long_description': "# Cairo-toolkit\n\nA set of useful tools for cairo / starknet development.\n\n- Generate / check the interfaces corresponding to your Starknet contracts.\n- Easily order your imports\n\n## Installation\n\n`pip install cairo-toolkit`\n\n## Usage\n\n```\ncairo-toolkit [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --version\n  --help     Show this message and exit.\n\nCommands:\n  check-interface\n  generate-interface\n  order-imports\n```\n\n### Generate interfaces\n\n```\nUsage: cairo-toolkit generate-interface [OPTIONS]\n\nOptions:\n  -f, --files TEXT      File paths\n  -p, --protostar       Uses `protostar.toml` to get file paths\n  -d, --directory TEXT  Output directory for the interfaces. If unspecified,\n                        they will be created in the same directory as the\n                        contracts\n  --help                Show this message and exit.\n```\n\n### Check existing interfaces\n\n```\nUsage: cairo-toolkit check-interface [OPTIONS]\n\nOptions:\n  --files TEXT          Contracts to check\n  -p, --protostar       Uses `protostar.toml` to get file paths\n  -d, --directory TEXT  Directory of the interfaces to check. Interfaces must\n                        be named `i_<contract_name>.cairo`\n  --help                Show this message and exit.\n```\n\n### Ordering imports in existing file\n\n```\nUsage: cairo-toolkit order-imports [OPTIONS]\n\nOptions:\n  -d, --directory TEXT  Directory with cairo files to format\n  -f, --files TEXT      File paths\n  -i, --imports TEXT    Imports order\n  --help                Show this message and exit.\n```\n\n## Example\n\nGenerate interfaces for the contracts in `contracts/` and put them in `interfaces/`:\n\n```\nfind contracts/ -iname '*.cairo' -exec cairo-toolkit generate-interface --files {} \\;\n```\n\nCheck the interface for `test/main.cairo` against the interface `i_main.cairo` in interfaces/:\n\n```\ncairo-toolkit check-interface --files test/main.cairo -d interfaces\n```\n\nOrder imports for all cairo files under `test`\n\n```\ncairo-toolkit order-imports -d test\n```\n\n## Protostar\n\nYou can use cairo-toolkit in a protostar project.\nThis can be paired with a github action to automatically generate the interfaces for the contracts\nthat specified inside the `protostar.toml` file.\n",
    'author': 'msaug',
    'author_email': 'msaug@protonmail.com',
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
