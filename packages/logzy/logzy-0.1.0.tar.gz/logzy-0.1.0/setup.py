# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logzy']

package_data = \
{'': ['*']}

install_requires = \
['astroid>=2.12.12,<3.0.0', 'libcst>=0.4.7,<0.5.0']

entry_points = \
{'console_scripts': ['logzy = logzy.app:main']}

setup_kwargs = {
    'name': 'logzy',
    'version': '0.1.0',
    'description': 'A tool for converting f-strings in log functions to lazy-logging',
    'long_description': '# Introduction\n\n*ALPHA SOFTWARE*: Use at your own risk. Carefully vet the suggestions.\n\n`logzy` is a linter / fixer that ensures Python log message arguments are in\nlazy-logging format. This is recommended so that arguments to the log messages\nare only rendered if they\'re emitted. Performance regressions can be occur if\nobjects are being rendered even if the log message isn\'t being emitted.\n\nFor example:\n\n```python\n\nimport logging\n\nlog = logging.getLogger()\n\nuser = "root"\n\n# Bad\nlog.warning(f"Login failed for {user}")\n\n# Good\nlog.warning("Login failed for %s", user)\n```\n\nYou may have seen tools like pylint complain about\n`logging-fstring-interpolation`, `logging-format-interpolation`, or\n`logging-not-lazy`.\n\n\n# Installation\n\n```sh\npip install logzy\n```\n\n# Usage\n\nSince logzy only works on f-strings right now, you probably want to convert\neverything to an f-string first using a tool like\n[flynt](https://github.com/ikamensh/flynt) or\n[pyupgrade](https://github.com/asottile/pyupgrade)\n\n\n# TODO\n\n* Non f-string parameters to log functions (ie `.format()` or `%`)\n* Untested f-strings:\n  * Multiline f-string\n  * Nested f-string\n',
    'author': 'Alex Harford',
    'author_email': 'harford@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
