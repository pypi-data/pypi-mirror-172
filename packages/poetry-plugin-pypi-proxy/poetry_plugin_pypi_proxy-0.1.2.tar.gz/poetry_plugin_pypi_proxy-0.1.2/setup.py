# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poetry_plugin_pypi_proxy']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0,<2.0.0']

entry_points = \
{'poetry.plugin': ['poetry-pypi-proxy = '
                   'poetry_plugin_pypi_proxy.plugin:PypiProxyPlugin']}

setup_kwargs = {
    'name': 'poetry-plugin-pypi-proxy',
    'version': '0.1.2',
    'description': 'Aliases PIP_INDEX_URL silently within Poetry to point at a new repository.',
    'long_description': '# poetry-plugin-pypi-proxy\n\nThis is a plugin that enables developers who use internal proxies of\nPypi to integrate their projects seamlessly with Poetry without\nneeding to build custom configurations for their proxy server.\n\nThe plugin operates intuitively -- users can onboard to this tooling\nby installing the plugin and then setting `PIP_INDEX_URL` before\nrunning Poetry commands.\n\nIt also runs silently, i.e., it will not pollute your `poetry.lock`\nwith the URL of your proxy server and `poetry publish` is\nautomatically redirected to the proxy as well.\n\n## Usage\n\nStart by installing Poetry with pipx:\n\n    pipx install poetry\n    pipx runpip poetry install poetry-plugin-pypi-proxy\n\nIf you have already installed poetry, you only need to run the second command.\n\nNow, any Poetry project will automatically use the proxy server\nspecified by `PIP_INDEX_URL`. You may add this to your `rc` file\n(`.bashrc`, `.zshrc`, `.envrc` with direnv, etc) or simply export it\nin your terminal to get started.\n',
    'author': 'Chad Crawford',
    'author_email': 'chad@cacrawford.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
