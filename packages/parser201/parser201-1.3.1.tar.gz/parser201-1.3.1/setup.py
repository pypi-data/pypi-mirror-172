# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['parser201']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'parser201',
    'version': '1.3.1',
    'description': 'Extract individual fields from lines in Apache access logs',
    'long_description': '![GitHub](https://img.shields.io/github/license/geozeke/parser201)\n![PyPI](https://img.shields.io/pypi/v/parser201)\n![PyPI - Status](https://img.shields.io/pypi/status/parser201)\n![GitHub last commit](https://img.shields.io/github/last-commit/geozeke/parser201)\n![GitHub issues](https://img.shields.io/github/issues/geozeke/parser201)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/parser201)\n![GitHub repo size](https://img.shields.io/github/repo-size/geozeke/parser201)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/parser201)\n\n<br>\n\n<img src="https://github.com/geozeke/parser201/blob/main/docs/logo.png?raw=true" width="120"/>\n\n## Features\n\nThe centerpiece of the parser201 module is the LogParser class. The class initializer takes a single line from an Apache access log file and extracts the individual fields into attributes within an object.\n\n## Installation\n\n```text\npip3 install parser201\n```\n\n## Usage\n\nThe most common use-case for parser201 is importing individual lines from an Apache access log file and creating LogParser objects, like this:\n\n```python\nfrom parser201 import LogParser\n\nwith open(\'access.log\', \'r\') as f:\n    for line in f:\n        lp = LogParser(line)\n        # Use lp as desired: add to List, Dictionary, etc.\n```\n\n## Documentation\n\nSee: [parser201 Documentation](https://geozeke.github.io/parser201).\n\n## Version History\n\n* 1.3.1 (2022-10-22)\n  * Migrated dependency/build management to [poetry](https://python-poetry.org/).<br><br>\n* 1.3.0 (2022-08-13)\n  * Implemented `__eq__` magic method for the `LogParser` class. You can now\n    perform equality checks on two `LogParser` objects.\n  * Added test cases for `__eq__`\n  * Migrated task runner to `make`\n  * Documentation cleanup\n  * Code linting and cleanup<br><br>\n* 1.2.0 (2022-07-17)\n  * Implemented `__eq__` magic methods in the `FMT` and `TZ` classes.\n  * Documentation cleanup.\n  * Testing improvements and pyproject.toml adjustments for better pytest compatability.\n  * Code linting and cleanup.<br><br>\n* 1.1.5 (2022-01-17)\n  * Code linting and cleanup.<br><br>\n* 1.1.4 (2021-12-23)\n  * Documentation cleanup.<br><br>\n* 1.1.3 (2021-12-19)\n  * Make file tuning.\n  * Documentation cleanup.\n  * Added site logo to README.md.<br><br>\n* 1.1.0 (2021-11-13)\n  * Implemented selectable timestamp conversion options {*original*, *local*, [*UTC*](https://en.wikipedia.org/wiki/Coordinated_Universal_Time)}.\n  * Implemented selectable formatting options for timestamp attribute {*string*, *date_obj*}.\n  * Migrated API reference to GitHub pages.\n  * Code cleanup.<br><br>\n* 1.0.2 (2021-11-05)\n  * Documentation cleanup.<br><br>\n* 1.0.0 (2021-11-04)\n  * Stable production release.\n  * Migrated to a new development framework.\n  * Implemented more robust and compartmentalized test cases.\n  * Code tuning.<br><br>\n* 0.2.0 (2021-10-31)\n  * Changed behavior to gracefully fail for any malformed input line. If an input line cannot be successfully parsed, all attributes of the returned object are set to `None` and no messages are printed.\n  * Added additional pytest cases to verify failure behavior.<br><br>\n* 0.1.9 (2021-09-15)\n  * Code cleanup for pep8 compliance.\n  * Cleaned up Makefiles and scripts to remove references to python (meaning python2) and replace it with python3.<br><br>\n* 0.1.7 (2021-06-05)\n  * Re-tooled testing scripts to use parameterized test data, and conduct more robust testing.<br><br>\n* 0.1.6 (2020-12-19)\n  * Addressed exception handling for initializer input not being a valid string data type.\n  * Documentation cleanup.<br><br>\n* 0.1.5 (2020-10-26)\n  * Enabled automatic deployment of tagged releases to pypi from travis using encrypted token.\n  * Converted references to the master branch in the git repository to main across the documentation set.\n  * Documentation cleanup.<br><br>\n* 0.1.4 (2020-10-24)\n  * Initial pypi release.\n  * Fixed test file filtering issue in .gitignore.\n  * Dependency fix for travis tests.<br><br>\n* 0.1.1 (2020-10-22)\n  * Follow-on testing on test.pypi.org.<br><br>\n* 0.1.0 (2020-10-18)\n  * Initial testing on test.pypi.org.\n',
    'author': 'Peter Nardi',
    'author_email': 'pete@nardi.com',
    'maintainer': 'Peter Nardi',
    'maintainer_email': 'pete@nardi.com',
    'url': 'https://github.com/geozeke/parser201',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
