# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['transformer_embeddings']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'transformer-embeddings',
    'version': '0.0.1',
    'description': 'Transformer Embeddings',
    'long_description': "# Transformer Embeddings\n\n[![PyPI](https://img.shields.io/pypi/v/transformer-embeddings.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/transformer-embeddings.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/transformer-embeddings)][python version]\n[![License](https://img.shields.io/pypi/l/transformer-embeddings)][license]\n\n[![Tests](https://github.com/ginger-io/transformer-embeddings/workflows/Tests/badge.svg?branch=main)][tests]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/transformer-embeddings/\n[status]: https://pypi.org/project/transformer-embeddings/\n[python version]: https://pypi.org/project/transformer-embeddings\n[read the docs]: https://transformer-embeddings.readthedocs.io/\n[tests]: https://github.com/ginger-io/transformer-embeddings/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/ginger-io/transformer-embeddings\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Transformer Embeddings_ via [pip] from [PyPI]:\n\n```console\n$ pip install transformer-embeddings\n```\n\n## Contributing\n\nContributions are very welcome. To learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [Apache 2.0 license][license], _Transformer Embeddings_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems, please [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was partly generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/ginger-io/transformer-embeddings/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/ginger-io/transformer-embeddings/blob/main/LICENSE\n[contributor guide]: https://github.com/ginger-io/transformer-embeddings/blob/main/CONTRIBUTING.md\n[command-line reference]: https://transformer-embeddings.readthedocs.io/en/latest/usage.html\n",
    'author': 'Headspace Health',
    'author_email': 'transformer-embeddings@headspace.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ginger-io/transformer-embeddings',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
