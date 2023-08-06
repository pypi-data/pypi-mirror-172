# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aea',
 'aea.cli',
 'aea.cli.registry',
 'aea.cli.utils',
 'aea.components',
 'aea.configurations',
 'aea.connections',
 'aea.connections.scaffold',
 'aea.context',
 'aea.contracts',
 'aea.contracts.scaffold',
 'aea.crypto',
 'aea.crypto.registries',
 'aea.decision_maker',
 'aea.error_handler',
 'aea.helpers',
 'aea.helpers.acn',
 'aea.helpers.ipfs',
 'aea.helpers.ipfs.pb',
 'aea.helpers.multiaddr',
 'aea.helpers.preference_representations',
 'aea.helpers.search',
 'aea.helpers.storage',
 'aea.helpers.storage.backends',
 'aea.helpers.transaction',
 'aea.identity',
 'aea.mail',
 'aea.manager',
 'aea.protocols',
 'aea.protocols.dialogue',
 'aea.protocols.generator',
 'aea.protocols.scaffold',
 'aea.registries',
 'aea.skills',
 'aea.skills.scaffold',
 'aea.test_tools']

package_data = \
{'': ['*'],
 'aea.configurations': ['schemas/*', 'schemas/configurable_parts/*'],
 'aea.helpers.storage.backends': ['binaries/*']}

install_requires = \
['base58>=1.0.3,<3.0.0',
 'ecdsa>=0.15,<0.17.0',
 'importlib-metadata>4,<5',
 'jsonschema>=4.0.0,<5.0.0',
 'packaging>=21.0,<22.0',
 'protobuf>=3.19.0,<=3.19.4',
 'pymultihash==0.8.2',
 'python-dotenv>=0.14.0,<0.18.0',
 'pyyaml>=4.2b1,<6.0',
 'requests>=2.22.0,<3.0.0',
 'semver>=2.9.1,<3.0.0']

extras_require = \
{':sys_platform == "win32" or platform_system == "Windows"': ['pywin32==303'],
 'all': ['click>=8.0.0,<9.0.0'],
 'cli': ['click>=8.0.0,<9.0.0']}

entry_points = \
{'console_scripts': ['aea = aea.cli:cli']}

setup_kwargs = {
    'name': 'aea',
    'version': '1.2.2',
    'description': 'Autonomous Economic Agent framework',
    'long_description': '<h1 align="center">\n    <b>AEA Framework</b>\n</h1>\n\n<p align="center">\n  <a href="https://pypi.org/project/aea/">\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/aea">\n  </a>\n  <a href="https://pypi.org/project/aea/">\n    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/aea">\n  </a>\n  <a>\n    <img alt="PyPI - Wheel" src="https://img.shields.io/pypi/wheel/aea">\n  </a>\n  <a href="https://github.com/fetchai/agents-aea/blob/main/LICENSE">\n    <img alt="License" src="https://img.shields.io/pypi/l/aea"> \n  </a>\n  <a href="https://pypi.org/project/aea/">\n    <img alt="License" src="https://img.shields.io/pypi/dm/aea"> \n  </a>\n  <a href="https://fetch-ai.slack.com/join/shared_invite/enQtNDI2MDYwMjE3OTQwLWY0ZjAyYjM0NGQzNWRhNDMxMzdjYmVhYTE3NDNhNTAyMTE0YWRkY2VmOWRmMGQ3ODM1N2NjOWUwNDExM2U3YjY">\n    <img alt="Slack" src="https://img.shields.io/badge/slack-fetchai-purple.svg">\n  </a>\n</p>\n<p align="center">\n  <a href="https://github.com/fetchai/agents-aea/workflows/AEA%20framework%20sanity%20checks%20and%20tests">\n    <img alt="AEA framework sanity checks and tests" src="https://github.com/fetchai/agents-aea/workflows/AEA%20framework%20sanity%20checks%20and%20tests/badge.svg?branch=main">\n  </a>\n  <a href="">\n    <img alt="Codecov" src="https://img.shields.io/codecov/c/github/fetchai/agents-aea">\n  </a>\n  <a href="https://img.shields.io/badge/lint-flake8-blueviolet">\n    <img alt="flake8" src="https://img.shields.io/badge/lint-flake8-yellow" >\n  </a>\n  <a href="https://github.com/python/mypy">\n    <img alt="mypy" src="https://img.shields.io/badge/static%20check-mypy-blue">\n  </a>\n  <a href="https://github.com/psf/black">\n    <img alt="Black" src="https://img.shields.io/badge/code%20style-black-black">\n  </a>\n  <a href="https://github.com/PyCQA/bandit">\n    <img alt="mypy" src="https://img.shields.io/badge/security-bandit-lightgrey">\n  </a>\n</p>\n\n<p align="center">\nA framework for autonomous economic agent (AEA) development\n</p>\n\n<p align="center">\n  <img src="/data/aea.png?raw=true" alt="AEA Description" width="70%"/>\n</p>\n\n## Get started developing AEAs\n\n1. Create and launch a clean virtual environment with Python 3.7 (any Python `>=` 3.6 works):\n\n       pipenv --python 3.7 && pipenv shell\n\n2. Install the package from [PyPI](https://pypi.org/project/aea/):\n\n       pip install aea[all]\n\n    Or, if you use `zsh` rather than `bash`:\n\n       pip install "aea[all]"\n\n3. Then, build your agent as described in the [docs](https://docs.fetch.ai/aea/).\n\n<p align="center">\n  <a href="https://www.youtube.com/embed/xpJA4IT5X88">\n    <img src="/data/video-aea.png?raw=true" alt="AEA Video" width="70%"/>\n  </a>\n</p>\n\n## Alternatively (1): Use `pipx` (CLI usage only)\n\n1. Install [pipx](https://github.com/pipxproject/pipx)\n\n2. Install the package from [PyPI](https://pypi.org/project/aea/):\n\n       pipx install aea[all]\n\n3. Run AEA CLI e.g.:\n\n       aea --help\n\n## Alternatively (2): Install from Source\n\nThis approach is not recommended!\n\n### Cloning\n\nThis repository contains submodules. Clone with recursive strategy:\n\n    git clone https://github.com/fetchai/agents-aea.git --recursive && cd agents-aea\n\n- To fetch/update submodules (for existing local repo):\n\n      git submodule sync --recursive && git submodule update --init --recursive\n\n### Dependencies\n\nAll python specific framework dependencies are specified in `setup.py` and installed with the framework. All development dependencies are specified in `Pipfile` (and installed via the commands specified in [Preliminaries](#preliminaries)).\n\nYou can have more control on the installed dependencies by leveraging the setuptools\' extras mechanism. \n\n### Preliminaries\n\n- Create and launch a virtual environment with Python 3.7 (any Python `>=` 3.6 works):\n\n      pipenv --python 3.7 && pipenv shell\n\n- Install the package from source:\n\n      pip install .[all]\n\n    Or, if you use `zsh` rather than `bash`:\n\n      pip install ".[all]"\n\n- Then, build your agent as described in the [docs](https://fetchai.github.io/agents-aea/).\n\n## Documentation\n\n- All documentation is hosted [here](https://docs.fetch.ai/aea).\n\n- To start a live-reloading docs server on localhost: `mkdocs serve`. To amend the docs, create a new documentation file in `docs/` and add a reference to it in `mkdocs.yml`.\n\n- To run demos against local packages use flag `--local` in `aea` CLI commands.\n\n## Contributing\n\nWe welcome contributions to the framework, its plugins, related tools and packages. Please consult the [contributing guide](https://github.com/fetchai/agents-aea/blob/main/CONTRIBUTING.md) for details.\n\n## Cite\n\nIf you are using our software in a publication, please \nconsider to cite it with the following BibTex entry:\n\n```\n@misc{agents-aea,\n  Author = {Marco Favorito and David Minarsch and Ali Hosseini and Aristotelis Triantafyllidis and Diarmid Campbell and Oleg Panasevych and Kevin Chen and Yuri Turchenkov and Lokman Rahmani and Jiří Vestfál and James Riehl},\n  Title = {Autonomous Economic Agent (AEA) Framework},\n  Year = {2019},\n}\n```\n',
    'author': 'Fetch.AI Limited',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fetchai/agents-aea',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
