# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prefect_redis']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.2.0,<3.0.0',
 'prefect>=2.0.0',
 'pytest-asyncio>=0.19.0,<0.20.0',
 'redis>=4.3.4']

setup_kwargs = {
    'name': 'prefect-redis',
    'version': '0.1.4',
    'description': 'Prefect integrations for working with Redis',
    'long_description': '# prefect-redis\n\n<p align="center">\n    <a href="https://pypi.python.org/pypi/prefect-redis/" alt="PyPI version">\n        <img alt="PyPI" src="https://img.shields.io/pypi/v/prefect-redis?color=0052FF&labelColor=090422"></a>\n    <a href="https://github.com/C4IROcean/prefect-redis/" alt="Stars">\n        <img src="https://img.shields.io/github/stars/C4IROcean/prefect-redis?color=0052FF&labelColor=090422" /></a>\n    <a href="https://pepy.tech/badge/prefect-redis/" alt="Downloads">\n        <img src="https://img.shields.io/pypi/dm/prefect-redis?color=0052FF&labelColor=090422" /></a>\n    <a href="https://github.com/C4IROcean/prefect-redis/pulse" alt="Activity">\n        <img src="https://img.shields.io/github/commit-activity/m/C4IROcean/prefect-redis?color=0052FF&labelColor=090422" /></a>\n    <br>\n    <a href="https://prefect-community.slack.com" alt="Slack">\n        <img src="https://img.shields.io/badge/slack-join_community-red.svg?color=0052FF&labelColor=090422&logo=slack" /></a>\n    <a href="https://discourse.prefect.io/" alt="Discourse">\n        <img src="https://img.shields.io/badge/discourse-browse_forum-red.svg?color=0052FF&labelColor=090422&logo=discourse" /></a>\n</p>\n\n## Welcome!\n\nPrefect integrations for working with Redis\n\n## Getting Started\n\n### Python setup\n\nRequires an installation of Python 3.7+.\n\nWe recommend using a Python virtual environment manager such as pipenv, conda or virtualenv.\n\nThese tasks are designed to work with Prefect 2.0. For more information about how to use Prefect, please refer to the [Prefect documentation](https://orion-docs.prefect.io/).\n\n### Installation\n\nInstall `prefect-redis` with `pip`:\n\n```bash\npip install prefect-redis\n```\n\nThen, register to [view the block](https://orion-docs.prefect.io/ui/blocks/) on Prefect Cloud:\n\n```bash\nprefect block register -m prefect_redis.credentials\n```\n\nNote, to use the `load` method on Blocks, you must already have a block document [saved through code](https://orion-docs.prefect.io/concepts/blocks/#saving-blocks) or [saved through the UI](https://orion-docs.prefect.io/ui/blocks/).\n\n### Write and run a flow\n\n```python\nfrom prefect import flow\nfrom prefect_redis import (\n    RedisCredentials,\n    redis_set,\n    redis_get,\n)\n\n\n@flow\ndef example_flow():\n    \n    # Load credentials-block\n    credentials = RedisCredentials.load("my-redis-store")\n    \n    # Set a redis-key - Supports any object that is not a live connection\n    redis_set(credentials, "mykey", {"foo": "bar"})\n    \n    # Get a redis key\n    val = redis_get(credentials, "mykey")\n    \n    print(val)\n\nexample_flow()\n```\n\n## Resources\n\nIf you encounter any bugs while using `prefect-redis`, feel free to open an issue in the [prefect-redis](https://github.com/C4IROcean/prefect-redis) repository.\n\nIf you have any questions or issues while using `prefect-redis`, you can find help in either the [Prefect Discourse forum](https://discourse.prefect.io/) or the [Prefect Slack community](https://prefect.io/slack).\n\nFeel free to ⭐️ or watch [`prefect-redis`](https://github.com/C4IROcean/prefect-redis) for updates too!\n\n## Development\n\nIf you\'d like to install a version of `prefect-redis` for development, clone the repository and perform an editable install with `pip`:\n\n```bash\ngit clone https://github.com/C4IROcean/prefect-redis.git\n\ncd prefect-redis/\n\npip install -e ".[dev]"\n\n# Install linting pre-commit hooks\npre-commit install\n```\n',
    'author': 'Thomas Li Fredriksen',
    'author_email': 'thomas.fredriksen@oceandata.earth',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
