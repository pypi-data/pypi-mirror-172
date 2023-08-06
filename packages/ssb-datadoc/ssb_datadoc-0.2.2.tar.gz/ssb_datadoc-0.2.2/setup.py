# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datadoc',
 'datadoc.backend',
 'datadoc.frontend',
 'datadoc.frontend.callbacks',
 'datadoc.frontend.components',
 'datadoc.frontend.fields',
 'datadoc.tests']

package_data = \
{'': ['*'],
 'datadoc': ['assets/*', 'assets/fonts/*'],
 'datadoc.tests': ['resources/*',
                   'resources/existing_metadata_file/*',
                   'resources/existing_metadata_file/compatibility/*',
                   'resources/existing_metadata_file/compatibility/v0_1_1/*',
                   'resources/existing_metadata_file/invalid_id_field/*',
                   'resources/existing_metadata_file/valid_id_field/*']}

install_requires = \
['dash-bootstrap-components>=1.1.0',
 'dash>=2.4.1',
 'jupyter-dash>=0.4.2',
 'pandas>=1.4.2',
 'pyarrow>=8.0.0',
 'pydantic>=1.9.1',
 'requests>=2.27.1',
 'ssb-datadoc-model==2.0.0']

extras_require = \
{'gcs': ['dapla-toolbelt>=1.3.3', 'gcsfs>=2022.7.1']}

entry_points = \
{'console_scripts': ['datadoc = datadoc.app:main']}

setup_kwargs = {
    'name': 'ssb-datadoc',
    'version': '0.2.2',
    'description': "Document dataset metadata. For use in Statistics Norway's metadata system.",
    'long_description': '# Datadoc\n\n![Datadoc Unit tests](https://github.com/statisticsnorway/datadoc/actions/workflows/unit-tests.yml/badge.svg) ![Code coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/mmwinther/0c0c5bdfc360b59254f2c32d65914025/raw/pytest-coverage-badge-datadoc.json) [![PyPI version](https://img.shields.io/pypi/v/ssb-datadoc)](https://pypi.org/project/ssb-datadoc/) ![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\nDocument datasets in Statistics Norway\n\n## Usage\n\n![DataDoc in use](./doc/change-language-example.gif)\n\n### From Jupyter\n\n1. Open <https://jupyter.dapla-staging.ssb.no> or another Jupyter Lab environment\n1. Run `pip install ssb-datadoc[gcs]` in the terminal\n1. Upload a dataset to your Jupyter server (e.g. <https://github.com/statisticsnorway/datadoc/blob/master/klargjorte_data/person_data_v1.parquet>)\n1. Run `from datadoc import main; main("./person_data_v1.parquet")` in a notebook\n1. Datadoc will open in a new tab\n\n## Contributing\n\n### Prerequisites\n\n- Python >3.8 (3.10 is preferred)\n- Poetry, install via `curl -sSL https://install.python-poetry.org | python3 -`\n\n### Dependency Management\n\nPoetry is used for dependency management. [Poe the Poet](https://github.com/nat-n/poethepoet) is used for running poe tasks within poetry\'s virtualenv. Upon cloning this project first install necessary dependencies, then run the tests to verify everything is working.\n\n#### Install all dependencies\n\n```shell\npoetry install --all-extras\n```\n\n### Add dependencies\n\n#### Main\n\n```shell\npoetry add <python package name>\n```\n\n#### Dev\n\n```shell\npoetry add --group dev <python package name>\n```\n\n### Run tests\n\n```shell\npoetry run poe test\n```\n\n### Run project locally\n\nTo run the project locally:\n\n```shell\npoetry run poe datadoc "gs://ssb-staging-dapla-felles-data-delt/datadoc/klargjorte_data/person_data_v1.parquet"\n```\n\n### Run project locally in Jupyter\n\nTo run the project locally in Jupyter run:\n\n```shell\npoetry run poe jupyter\n```\n\nA Jupyter instance should open in your browser. Open and run the cells in the `.ipynb` file to demo datadoc.\n\n### Bump version\n\n```shell\npoetry run poe bump-patch-version\n```\n\n> :warning: Run this on the default branch\n\nThis command will:\n\n1. Increment version strings in files\n1. Commit the changes\n1. Tag the commit with the new version\n\nThen just run `git push origin --tags` to push the changes and trigger the release process.\n',
    'author': 'Statistics Norway',
    'author_email': 'stat-dev@ssb.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/statisticsnorway/datadoc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
