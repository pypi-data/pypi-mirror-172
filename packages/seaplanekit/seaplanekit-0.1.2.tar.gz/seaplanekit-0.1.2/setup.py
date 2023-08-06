# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['seaplanekit',
 'seaplanekit.api',
 'seaplanekit.logging',
 'seaplanekit.model',
 'seaplanekit.model.compute',
 'seaplanekit.model.locks',
 'seaplanekit.model.metadata',
 'seaplanekit.model.restrict',
 'seaplanekit.util']

package_data = \
{'': ['*']}

install_requires = \
['attrs==21.4.0',
 'certifi==2022.6.15',
 'charset-normalizer==2.1.0',
 'idna==3.3',
 'iniconfig==1.1.1',
 'packaging==21.3',
 'pluggy==1.0.0',
 'py==1.11.0',
 'pyparsing==3.0.9',
 'requests-mock>=1.9.3,<2.0.0',
 'requests==2.28.1',
 'returns>=0.19.0,<0.20.0',
 'simplejson>=3.17.6,<4.0.0',
 'tomli==2.0.1',
 'types-requests>=2.28.0,<3.0.0',
 'types-simplejson>=3.17.7,<4.0.0',
 'urllib3==1.26.9']

setup_kwargs = {
    'name': 'seaplanekit',
    'version': '0.1.2',
    'description': 'Seaplane Python SDK',
    'long_description': '# Seaplane Python SDK\n\nSimple Python library to manage your resources at seaplane.\n\n## What is Seaplane?\n\nSeaplane is the global platform for building and scaling your application stack\nwithout the complexity of managing cloud infrastructure.\n\nIt serves as a reference application for how our APIs can be utilized.\n\nNot sure where to go to quickly run a workload on Seaplane? See our [Getting\nStarted] guide.\n\n### Dependencies\n\nInstall dependencies\n\n```\n$ poetry install\n```\n\nTo [activate](https://python-poetry.org/docs/basic-usage#activating-the-virtual-environment) the virtual environment that is automatically created by Poetry:\n\n```\n$ poetry shell\n```\n\nTo deactivate the environment:\n\n```\n(seaplane) $ exit\n```\n\nTo upgrade all dependencies to their latest versions:\n\n```\n$ poetry update\n```\n\n## Packaging\n\nTo package the project as both a source distribution and a wheel:\n\n```\n$ poetry build\n```\n\nThis will generate `dist/fact-1.0.0.tar.gz` and `dist/fact-1.0.0-py3-none-any.whl`.\n\nSource and wheel redistributable packages can be [published to PyPI](https://python-poetry.org/docs/cli#publish) or installed directly from the filesystem using pip.\n\n```\n$ poetry publish\n```\n\n## Enforcing Code Quality\n\nAutomated code quality checks are performed using [Nox](https://nox.thea.codes/en/stable/) and [nox-poetry](https://nox-poetry.readthedocs.io/en/stable/)\n\nTo run all default sessions:\n\n> Note: nox is installed into the virtual environment automatically by the poetry install command above. Run poetry shell to activate the virtual environment.\n\n```\n(seaplane) $ nox\n```\n\n## Testing\n\nTo pass arguments to pytest through nox:\n\n```\n(seaplane) $ nox -s test -- -k invalid_factorial\n```\n\nTo run end to end tests you have to set the E2E_API_KEY env var:\n\n```\n(seaplane) $ export E2E_API_KEY="sp-your_api_key"\n(seaplane) $ nox -s e2e\n```\n\n## Code Style Checking\n\n[PEP 8](https://peps.python.org/pep-0008/) is the universally accepted style guide for\nPython code. PEP 8 code compliance is verified using [Flake8](http://flake8.pycqa.org/). Flake8 is\nconfigured in the `[tool.flake8]` section of `pyproject.toml`. Extra Flake8 plugins are also\nincluded:\n\n- `flake8-bugbear`: Find likely bugs and design problems in your program.\n- `flake8-broken-line`: Forbid using backslashes (`\\`) for line breaks.\n- `flake8-comprehensions`: Helps write better `list`/`set`/`dict` comprehensions.\n- `pep8-naming`: Ensure functions, classes, and variables are named with correct casing.\n- `pyproject-flake8`: Allow configuration of `flake8` through `pyproject.toml`.\n\nTo lint code, run:\n\n```bash\n(seaplane) $ nox -s lint\n```\n\n## Automated Code Formatting\n\nCode is automatically formatted using [black](https://github.com/psf/black). Imports are\nautomatically sorted and grouped using [isort](https://github.com/PyCQA/isort/).\n\nThese tools are configured by:\n\n- [`pyproject.toml`](./pyproject.toml)\n\nTo automatically format code, run:\n\n```bash\n(fact) $ nox -s fmt\n```\n\nTo verify code has been formatted, such as in a CI job:\n\n```bash\n(fact) $ nox -s fmt_check\n```\n\n## Type Checking\n\n[Type annotations](https://docs.python.org/3/library/typing.html) allows developers to include\noptional static typing information to Python source code. This allows static analyzers such\nas [mypy](http://mypy-lang.org/), [PyCharm](https://www.jetbrains.com/pycharm/),\nor [Pyright](https://github.com/microsoft/pyright) to check that functions are used with the correct types before runtime.\n\nmypy is configured in [`pyproject.toml`](./pyproject.toml). To type check code, run:\n\n```bash\n(fact) $ nox -s type_check\n```\nSee also [awesome-python-typing](https://github.com/typeddjango/awesome-python-typing).\n\n\n## Configure your API KEY\n\n* Set `SEAPLANE_API_KEY` environment variable.\n* Use `config` object in order to set the api key.\n\n```python\nfrom seaplanekit import sea\n\nsea.config.set_api_key("your_api_key")\n```\n\n## License\n\nLicensed under the Apache License, Version 2.0, [LICENSE](LICENSE). Copyright 2022 Seaplane IO, Inc.\n\n[//]: # (Links)\n\n[Seaplane]: https://seaplane.io/\n[CLI]: https://github.com/seaplane-io/seaplane/tree/main/seaplane-cli\n[SDK]: https://github.com/seaplane-io/seaplane/tree/main/seaplane\n[Getting Started]: https://github.com/seaplane-io/seaplane/blob/main/docs/GETTING_STARTED.md\n',
    'author': 'Seaplane IO, Inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/seaplane-io/seaplane/tree/main/seaplane-sdk/python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
