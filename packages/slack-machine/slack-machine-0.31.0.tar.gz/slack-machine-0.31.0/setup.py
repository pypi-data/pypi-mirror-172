# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['machine',
 'machine.bin',
 'machine.clients',
 'machine.models',
 'machine.plugins',
 'machine.plugins.builtin',
 'machine.plugins.builtin.fun',
 'machine.storage',
 'machine.storage.backends',
 'machine.utils']

package_data = \
{'': ['*']}

install_requires = \
['APScheduler>=3.9.1,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'dill>=0.3.5.1,<0.4.0.0',
 'httpx>=0.23.0,<0.24.0',
 'pydantic>=1.10.2,<2.0.0',
 'pyee>=9.0.4,<10.0.0',
 'slack-sdk>=3.18.1,<4.0.0',
 'structlog>=22.1.0,<23.0.0',
 'tzdata>=2022.2,<2023.0']

extras_require = \
{':python_version < "3.9"': ['backports.zoneinfo>=0.2.1,<0.3.0'],
 'dynamodb': ['aioboto3>=10.0.0,<11.0.0'],
 'redis': ['redis>=4.3.4,<5.0.0', 'hiredis>=2.0.0,<3.0.0']}

entry_points = \
{'console_scripts': ['slack-machine = machine.bin.run:main']}

setup_kwargs = {
    'name': 'slack-machine',
    'version': '0.31.0',
    'description': 'A wonderful, simple, yet powerful and extendable Slack bot framework',
    'long_description': '# Slack Machine\n\n[![Join the chat at Slack](https://img.shields.io/badge/chat-slack-green?logo=slack&logoColor=white)](https://join.slack.com/t/slack-machine-chat/shared_invite/zt-1g87tzvlf-8bV_WnY3JZyaYNnRFwRd~w)\n[![image](https://img.shields.io/pypi/v/slack-machine.svg)](https://pypi.python.org/pypi/slack-machine)\n[![image](https://img.shields.io/pypi/l/slack-machine.svg)](https://pypi.python.org/pypi/slack-machine)\n[![image](https://img.shields.io/pypi/pyversions/slack-machine.svg)](https://pypi.python.org/pypi/slack-machine)\n[![CI Status](https://github.com/DonDebonair/slack-machine/actions/workflows/ci.yml/badge.svg)](https://github.com/DonDebonair/slack-machine/actions/workflows/ci.yml)\n[![image](https://codecov.io/gh/DonDebonair/slack-machine/branch/main/graph/badge.svg)](https://codecov.io/gh/DonDebonair/slack-machine)\n\nSlack Machine is a simple, yet powerful and extendable Slack bot framework. More than just a bot, Slack\nMachine is a framework that helps you develop your Slack workspace into a ChatOps powerhouse. Slack Machine is built\nwith an intuitive plugin system that lets you build bots quickly, but also allows for easy code organization. A\nplugin can look as simple as this:\n\n```python\nfrom machine.plugins.base import MachineBasePlugin, Message\nfrom machine.plugins.decorators import respond_to\n\nclass DeploymentPlugin(MachineBasePlugin):\n    """Deployments"""\n    @respond_to(r"deploy (?P<application>\\w+) to (?P<environment>\\w+)")\n    async def deploy(self, msg: Message, application, environment):\n        """deploy <application> <environment>: deploy application to target environment"""\n        await msg.say(f"Deploying {application} to {environment}")\n```\n\n## *Note*\n\nAs of v0.30.0 Slack Machine dropped support for the old backend based on the RTM API. As such, Slack Machine is now\nfully based on [AsyncIO](https://docs.python.org/3/library/asyncio.html). This means plugins written before the\nrewrite to asyncio aren\'t supported anymore. See [here](https://dondebonair.github.io/slack-machine/migrating/) for\na migration guide to get your old plugins working with the new version of Slack Machine.\n\nIt\'s really easy!\n\n## Features\n\n- Get started with mininal configuration\n- Built on top of the [Slack Events API](https://api.slack.com/apis/connections/events-api) for smoothly responding\n  to events in semi real-time. Uses [Socket Mode](https://api.slack.com/apis/connections/socket) so your bot doesn\'t\n  need to be exposed to the internet!\n- Support for rich interactions using the [Slack Web API](https://api.slack.com/web)\n- High-level API for maximum convenience when building plugins\n- Low-level API for maximum flexibility\n- Built on top of [AsyncIO](https://docs.python.org/3/library/asyncio.html) to ensure good performance by handling\n  communication with Slack concurrently\n\n### Plugin API features:\n\n- Listen and respond to any regular expression\n- Capture parts of messages to use as variables in your functions\n- Respond to messages in channels, groups and direct message conversations\n- Respond with reactions\n- Respond in threads\n- Respond with ephemeral messages\n- Send DMs to any user\n- Support for [blocks](https://api.slack.com/reference/block-kit/blocks)\n- Support for [message attachments](https://api.slack.com/docs/message-attachments) [Legacy 🏚]\n- Listen and respond to any [Slack event](https://api.slack.com/events) supported by the Events API\n- Store and retrieve any kind of data in persistent storage (currently Redis, DynamoDB and in-memory storage are\n  supported)\n- Schedule actions and messages\n- Emit and listen for events\n- Help texts for Plugins\n\n### Coming Soon\n\n- Support for Interactive Buttons\n- ... and much more\n\n## Installation\n\nYou can install Slack Machine using pip:\n\n``` bash\n$ pip install slack-machine\n```\n\nor add it to your [Poetry](https://python-poetry.org/) project:\n\n```bash\npoetry add slack-machine\n```\n\nIt is **strongly recommended** that you install `slack-machine` inside a\n[virtual environment](https://docs.python.org/3/tutorial/venv.html)!\n\n## Usage\n\n1. Create a directory for your Slack Machine bot: `mkdir my-slack-bot && cd my-slack-bot`\n2. Add a `local_settings.py` file to your bot directory: `touch local_settings.py`\n3. Create a new app in Slack: <https://api.slack.com/apps>\n4. Choose to create an app from an _App manifest_\n5. Copy/paste the following manifest: [`manifest.yaml`](docs/extra/manifest.yaml)\n6. Add the Slack App and Bot tokens to your `local_settings.py` like this:\n\n    ``` title="local_settings.py"\n    SLACK_APP_TOKEN = "xapp-my-app-token"\n    SLACK_BOT_TOKEN = "xoxb-my-bot-token"\n    ```\n\n7. Start the bot with `slack-machine-async`\n8. ...\n9. Profit!\n\n## Documentation\n\nYou can find the documentation for Slack Machine here: https://dondebonair.github.io/slack-machine/\n\nGo read it to learn how to properly configure Slack Machine, write plugins, and more!\n',
    'author': 'Daan Debie',
    'author_email': 'daan@dv.email',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DonDebonair/slack-machine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
