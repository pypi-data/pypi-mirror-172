# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memory_magics', 'memory_magics.memory_tracer']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=8.5.0,<9.0.0', 'psutil>=5.9.3,<6.0.0']

setup_kwargs = {
    'name': 'ipython-memory-magics',
    'version': '0.3.7',
    'description': 'IPython magic commands for tracking memory usage',
    'long_description': "# IPython memory magic commands\n\n[![PyPI](https://img.shields.io/pypi/v/ipython-memory-magics?color=brightgreen)](https://pypi.org/project/ipython-memory-magics/)\n\nSimple tool to trace memory usage of a Python statement or expression execution.\n\nMemory equivalent of IPython built-in [time magics](https://github.com/ipython/ipython/blob/66aeb3fc55c8ac04242e566172af5de5cc6fe71e/IPython/core/magics/execution.py#L1193). \n\nExisting tools like [memory-profiler](https://github.com/pythonprofilers/memory_profiler) or [ipython-memory-usage](https://github.com/ianozsvald/ipython_memory_usage) mainly use psutil package to measure memory usage, which may give inaccurate results. This package uses [tracemalloc](https://docs.python.org/3/library/tracemalloc.html) module to trace Python memory allocations. Memory-profiler provides tracemalloc backend, but it does not allow to use it for magic commands. This packages offers line `%memory` and cell `%%memory` magic commands, which were intended to complement the `%time` and `%%time` magic commands.\n\n# Installation\n\nInstall from pip:\n\n```\npip install ipython-memory-magics\n```\n\nOr install directly from github:\n\n```\npip install git+https://github.com/rusmux/ipython-memory-magics.git\n```\n\nAfter the installation load the extension via:\n\n```\n%load_ext memory_magics\n```\n\nTo activate it whenever you start IPython, edit the configuration file for your IPython profile `~/.ipython/profile_default/ipython_config.py`. Register the extension like this:\n\n```\nc.InteractiveShellApp.extensions = [\n    'memory_magics',\n]\n```\n\nIf the file does not already exist, run `ipython profile create` in a terminal.\n\n# Usage\n\nUse `%memory [options] statement` to measure `statement`'s memory consumption:\n\n```python\n%memory -q list(range(10**6))\n```\n\nThe output in the format `current / peak` will follow:\n\n```\nRAM usage: line: 34.33 MiB / 34.33 MiB\n```\n\nHere `-q` is the `quiet` flag set to suppress the output. You can use other options to get data on the notebook and jupyter memory usage, or to print the statistics in a table. For example, you can use `-n` or `--notebook` flag to get the information about the notebook current memory consumption:\n\n```python\n%memory -n\n```\n```\nRAM usage: notebook: 101.41 MiB\n```\n\nIn the same way, `-j` or `--jupyter` flag will give you the information about the total Jupyter memory usage.\n\nPut `%%memory [options]` on top of a cell to measure its memory consumption:\n\n```python\nIn [1]: %%memory -n -j -t\n        sum(list(range(10**6)))\n```\n\nThis will print:\n\n```\nRAM usage |   current   |     peak     |\n----------------------------------------\n cell     | 2.62 KiB    | 34.33 MiB    |\n notebook | 123.08 MiB  | 155.53 MiB   |\n jupyter  | 170.19 MiB  | 202.55 MiB   |\n\nOut [1]: 499999500000\n```\n\n# Options\n\nFive options are available in full and short versions:\n\n`-n <notebook>`: If present, show current notebook memory usage\n\n`-j <jupyter>`: If present, show current jupyter memory usage\n\n`-i <interval>`: Interval in milliseconds for updating memory usage information\n\n`-t <table>`: If present, print statistics in a table\n\n`-q <quiet>`: If present, do not return the output\n",
    'author': 'Ruslan Mukhametshin',
    'author_email': 'rusmux21@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rusmux/ipython-memory-magics',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
