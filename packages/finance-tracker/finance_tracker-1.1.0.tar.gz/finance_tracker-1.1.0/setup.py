# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['finance_tracker',
 'finance_tracker.aggregators',
 'finance_tracker.categories',
 'finance_tracker.entries',
 'finance_tracker.money',
 'finance_tracker.readers']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.13,<2.0.0', 'inquirer>=2.10.0,<3.0.0', 'pandas>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'finance-tracker',
    'version': '1.1.0',
    'description': 'Python tool to track finances over a year',
    'long_description': '# finance-tracker\n\nPython tool to track finances over a year\n\n[![PyPI](https://img.shields.io/pypi/v/finance-tracker)](https://pypi.org/project/finance-tracker/)\n[![GitHub release (latest by date)](https://img.shields.io/github/v/release/w0rmr1d3r/finance-tracker)](https://github.com/w0rmr1d3r/finance-tracker/releases)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/finance-tracker)\n[![CI](https://github.com/w0rmr1d3r/finance-tracker/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/w0rmr1d3r/finance-tracker/actions/workflows/ci.yml)\n[![CI](https://github.com/w0rmr1d3r/finance-tracker/actions/workflows/pylint.yml/badge.svg?branch=master)](https://github.com/w0rmr1d3r/finance-tracker/actions/workflows/pylint.yml)\n![GitHub last commit](https://img.shields.io/github/last-commit/w0rmr1d3r/finance-tracker)\n[![PyPi downloads](https://img.shields.io/pypi/dm/finance-tracker?label=PyPi%20downloads)](https://pypistats.org/packages/finance-tracker)\n\n## Installation\n\n### PyPi package\n\n```bash\npip install finance-tracker\n```\n\n## Usage\n\n### From repository\n\n1. Clone the repo\n2. Install [poetry](https://python-poetry.org)\n3. Run `make install`\n4. Load the categories and categories to filter as incomes wanted in a file called `categories.json`\n   in `./load/categories/`. Such as:\n    ```json\n    {\n      "CATEGORIES": {\n        "CATEGORY_ONE": [\n          "TITLE TO CATEGORIZE"\n        ],\n        "CATEGORY_TWO": [\n          "TITLE 2 TO CATEGORIZE"\n        ]\n      },\n      "POSITIVE_CATEGORIES": [\n        "CATEGORY_TWO"\n      ]\n    }\n    ```\n\n5. Load your CSV files according to your bank under `./load/entries_files/{bank}` according to your bank.\n   See [Banks Supported](#banks-supported).\n\n6. Load any other CSV files in the folder `./load/entries_files/`. By default, those files will have this format:\n    ```csv\n    HEADER1;;;;;\n    HEADER2;;;;;\n    DATE;DATE TWO;TITLE;OTHER DATA;QUANTITY;OTHER\n    01/01/1999;01/01/1999;PAYCHECK;PAYCHECK FROM COMPANY 1;1.000;1.000\n    ```\n\n7. Run `make run` and enjoy!\n\n### From package installation\n\n1. Follow the steps in [Installation](#installation)\n2. Load the categories and categories to filter as incomes wanted in a file called `categories.json`\n   in `./load/categories/`. Such as:\n    ```json\n    {\n      "CATEGORIES": {\n        "CATEGORY_ONE": [\n          "TITLE TO CATEGORIZE"\n        ],\n        "CATEGORY_TWO": [\n          "TITLE 2 TO CATEGORIZE"\n        ]\n      },\n      "POSITIVE_CATEGORIES": [\n        "CATEGORY_TWO"\n      ]\n    }\n    ```\n\n3. Load your CSV files according to your bank under `./load/entries_files/{bank}` according to your bank.\n   See [Banks Supported](#banks-supported).\n\n4. Load any other CSV files in the folder `./load/entries_files/`. By default, those files will have this format:\n    ```csv\n    HEADER1;;;;;\n    HEADER2;;;;;\n    DATE;DATE TWO;TITLE;OTHER DATA;QUANTITY;OTHER\n    01/01/1999;01/01/1999;PAYCHECK;PAYCHECK FROM COMPANY 1;1.000;1.000\n    ```\n\n5. Import it and use it in your project like this:\n    ```python\n    from finance_tracker.__main__ import run\n\n    if __name__ == "__main__":\n        run()\n    ```\n\n## Banks supported\n\n_Any other bank needs to be implemented or follow the current default CSV_\n\n- Revolut\n\n## Contributing\n\nPull requests are welcome. Issues are welcome too.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'w0rmr1d3r',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/w0rmr1d3r/finance-tracker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
