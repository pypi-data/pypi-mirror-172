# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandoc_run_python']

package_data = \
{'': ['*']}

install_requires = \
['panflute>=2.0.5,<3.0.0']

entry_points = \
{'console_scripts': ['pandoc-run-python = pandoc_run_python.filter:main']}

setup_kwargs = {
    'name': 'pandoc-run-python',
    'version': '0.1.4',
    'description': 'run python code blocks in markdown code',
    'long_description': '![PyPI](https://img.shields.io/pypi/v/pandoc-run-python)\n![CICD](https://github.com/Bart6114/pandoc-run-python/actions/workflows/publish.yml/badge.svg)\n[![Downloads](https://pepy.tech/badge/pandoc-run-python)](https://pepy.tech/project/pandoc-run-python)\n\n# pandoc-run-python\n\nThis is a [Pandoc filter](https://pandoc.org/filters.html)! \n\nMore specifically it is a filter that allows you to run Python code blocks in your markdown and insert the output of them back into your markdown file. It exists because I enjoy literate programming too much.\n\nIt supports capturing the following output of Python code blocks:\n- anything printed to `stdout`\n- matplotlib-based figures\n\n## Warning 🚨\n\nMake sure that you trust the Python code in your markdown files, they will be executed as-is. A cell with content like `os.system("sudo rm -rf /")` would be painful.\n\n## How to install\n\n```sh\npip install pandoc-run-python\n```\n\n## What does it do?\n\n\nLet\'s say you have the following markdown file:\n\n````md\n\n## What is fast, loud and crunchy?\n\n```python\nprint("A rocket chip!")\n```\n\n````\n\nWhen you use this as en example to explain what the output of this `print` statement would be, you\'d probably don\'t want to type the expected output of this command manually. Ideally you want it to be actually evaluated and the output inserted into the markdown file. This way you would automatically end up with something like this:\n\n````md\n\n## What is fast, loud and crunchy?\n\n```python\nprint("A rocket chip!")\n```\n\n```\nA rocket chip!\n```\n\n````\n\n## pandoc-run-python to the rescue!\n\nCoincidentally, the above is exactly what the `pandoc-run-python` filter provides. How can you achieve this? You need to slightly alter your markdown to specify that a python codeblock needs to be evaluated. More specifically you need to add classes to the codeblock as we did below (I don\'t like the syntax neither, but this is the pandoc way to do it).\n\n\n````md\n\n## What is fast, loud and crunchy?\n\n``` {.python .run}\nprint("A rocket chip!")\n```\n\n````\n\nIf the previous example would be in a file call `loud.md`, using this pandoc filter you could execute the following command to generate the processed markdown.\n\n```sh\npandoc loud.md -F pandoc-run-python -t markdown\n```\n\n````md\n## What is fast, loud and crunchy?\n\n``` {.python .run}\nprint("A rocket chip!")\n```\n\n``` {.python-output}\nA rocket chip!\n```\n````\n\n## Auto-formatting\n\nBy default, `black` is run on all code chunks denoted with `python` also those that do not have the `run` class.\n\n## Code chunk configuration\n\nThis filter runs on all code chunks that has at least the `python` and `run` class.\n\nThe following classes are used to determine filter logic:\n\n- `python` and `run`: evaluate code and insert output in a new codeblock / image below the original `python` codeblock\n- `no-black`: skip running of the black formatter on python code chunks',
    'author': 'Bart Smeets',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Bart6114/pandoc-run-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
