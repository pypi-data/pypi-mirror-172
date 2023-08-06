# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioburst']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0', 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'aioburst',
    'version': '0.2.0',
    'description': 'A library to optimize the speed of rate limited async calls.',
    'long_description': '# aioburst\nA library to optimize the speed of rate limited async calls, by alternating between bursts and sleeps.\n\n## Usage\n\nInstall the package using pip:\n\n`pip install aioburst`\n\nImport the limiter:\n\n`from aioburst import aioburst`\n\nInstantiate the limiter using the `create` method, setting the `limit` (number of calls) and `period` (period over \nwhich the number of calls are restricted):\n\n```\nlimiter = AIOBurst.create(limit=10, period=1.0)\n\nasync with limiter:\n    ...\n```\n<!-- #TODO: Add Graph showing how this works-->\n\nThe code above would allow 10 asynchronous entries (into the context manager) without any limit. Then it adds \n"sleepers" for the next calls. The sleeper tells the next entry when it can start. The 11th call gets the sleeper \nset by the 1st call that returned and waits until the `period` has elapsed. This approach ensures that there are\nnever more than `limit` simultaneous calls but that the next call can start as soon as possible. The result is that \nin a sliding window of `period` you should see exactly `limit` calls as active, regardless of how fast or slow any \nindividual call returns. \n\nYou can also stack limiters:\n\n```\nlimiter1 = AIOBurst.create(limit=10, period=1.0)\nlimiter2 = AIOBurst.create(limit=100, period=60.0)\n\nasync with limiter1:\n\tasync with limiter2:\n    ...\n```\n\n<!-- #TODO: Add Graph showing how this works-->\n\nUse this for cases where an API has a two-level rate limit like 10 calls per second or 100 calls per minute---both \nlimits will be respected. The stack is also idempotent, meaning that whichever way you stack the limiters, both \nlimits will be respected:\n\n```\nlimiter1 = AIOBurst.create(limit=10, period=1.0)\nlimiter2 = AIOBurst.create(limit=100, period=60.0)\n\n\nasync with limiter1:\n\tasync with limiter2:\n    ...\n    \n# The limit above will do the exact same thing as the limit below\nasync with limiter2:\n\tasync with limiter1:\n    ...\n```\n\n<!-- #TODO: Add Graph showing how this works-->',
    'author': 'ericfeunekes',
    'author_email': 'ericwill.f@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
