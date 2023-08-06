# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py_np4vtt']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'numdifftools>=0.9.40,<0.10.0',
 'pandas>=1.3.1,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'py-np4vtt',
    'version': '1.0.0',
    'description': 'Python library providing NonParametric models for Value of Travel Time analysis',
    'long_description': '# PyNP4VTT\n\nPython library providing NonParametric models for Value of Travel Time analysis.\n\n## Installation steps\n\n* Use `pip` to install the `py-np4vtt` library normally.\n  + Recommended: do it in a fresh virtual environment\n    - Create env: `python3 -m venv <chosen_venv_directory>`\n    - Activate env: `source <chosen_venv_directory>/bin/activate`\n  + Either install from TestPyPI\n    - `python3 -m pip install --index-url https://test.pypi.org/simple --extra-index-url https://pypi.org/simple py-np4vtt`\n  + Or from the normal (public/official) PyPI\n    - `python3 -m pip install py-np4vtt`\n\n## Instructions for contributing to the project\n\n### One-time setup\n\n* This project uses `poetry` as its dependency management, virtualenv management and release (build) tool\n   + Install following the steps described in https://python-poetry.org/docs/master/#installing-with-the-official-installer\n* Setup PyPI credentials to be able to publish packages\n   1. Make an account on `https://pypi.org`. Ask (optional) for invitation to become contributor on PyPI.\n   2. Add API token on the "account settings" page of PyPI (global scope)\n   3. Setup Poetry:\n      - `poetry config pypi-token.pypi "<your_api_token>"`\n* Setup TestPyPI credentials to be able to publish packages\n   1. Make an account on `https://test.pypi.org`. Ask (optional) for invitation to become contributor on TestPyPI.\n   2. Add API token on the "account settings" page of TestPyPI (global scope)\n   3. Setup Poetry:\n      - `poetry config repositories.testpypi https://test.pypi.org/legacy`\n      - `poetry config pypi-token.testpypi "<your_api_token>"`\n\n### Sometimes: update package dependencies\n\n* It is advisable to sometimes (every couple of months) update the package\'s dependencies\n  + Using newer versions (if possible) of dependencies gives you security fixes (sometimes also performance improvements)\n* Steps:\n  1. Make a backup of the lock file (in case you need to rollback the update):\n     - `mv poetry.lock bkp-poetry.lock`\n  2. Then create a new lock file with updated versions of dependencies, and install all fresh:\n     - `poetry update --lock`\n     - `poetry env remove python && poetry install`\n  3. Test that the program still works as expected\n  4. If the program breaks after the update, revert to the previous state by restoring the old lock file:\n     - `mv bkp-poetry.lock poetry.lock`\n     - `poetry env remove python && poetry install`\n  5. If nothing is broken after the update, remove the old lock file:\n     - `rm bkp-poetry.lock`\n\n### Building a new version and releasing/uploading to PyPI or TestPyPI\n\n1. Do the actual contribution to the project 🙂\n2. Increment the package\'s version number in `pyproject.toml`\n3. Build the package (wheel and source): `poetry build`. The built artifacts will be placed in the `dist` folder\n4. Publish:\n   + Either to PyPI: `poetry publish`\n   + Or to TestPyPI: `poetry publish -r testpypi`\n\n',
    'author': 'João Paulo Pizani Flor',
    'author_email': 'paulopizani@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.tudelft.nl/np4vtt/py-np4vtt',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.10',
}


setup(**setup_kwargs)
