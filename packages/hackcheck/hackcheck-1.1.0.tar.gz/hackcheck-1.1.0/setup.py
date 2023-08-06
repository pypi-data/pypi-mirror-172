# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hackcheck']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'hackcheck',
    'version': '1.1.0',
    'description': 'Official API wrapper for hackcheck.io',
    'long_description': '# Hackcheck-py\nOfficial python library for the [hackcheck.io](https://hackcheck.io) API\n\n- [Hackcheck-py](#hackcheck-py)\n  - [Installation](#installation)\n  - [Quick start](#quick-start)\n  - [Methods](#methods)\n\n\n## Installation\n\nInstall with pip\n\n```sh\npip install hackcheck\n```\n\n## Quick start\n\n```py\nfrom hackcheck import Hackcheck\n\n# Get an api key by purchasing a developer plan https://hackcheck.io/plans\nhc = Hackcheck("MY_API_KEY")\n\nresult = hc.lookup_email("your@email.com")\n\nfor r in result:\n    print(f"Database: {r.source.name}")\n    print(f"Date: {r.source.date}")\n    print(f"Password: {r.password}")\n    print(f"Username: {r.username}")\n    print(f"IP: {r.ip}")\n    print("------")\n\n# Check your ratelimits\nprint(f"Current rate limit: {hc.current_rate_limit}")\nprint(f"Allowed rate limit: {hc.allowed_rate_limit}")\n```\n\n## Methods\n\n```py\nhc.lookup_email("your@email.com")\nhc.lookup_username("username")\nhc.lookup_password("password")\nhc.lookup_name("Full Name")\nhc.lookup_ip("8.8.8.8")\nhc.lookup_phone("1234567890")\nhc.lookup_domain("hackcheck.io")\n```\n',
    'author': 'balluh',
    'author_email': 'revoked@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hackcheckio/hackcheck-py/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
