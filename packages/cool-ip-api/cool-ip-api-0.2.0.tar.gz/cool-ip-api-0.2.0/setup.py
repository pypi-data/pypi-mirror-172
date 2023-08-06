# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cool_ip_api', 'cool_ip_api.provider', 'cool_ip_api.utils']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'pydantic>=1.10.2,<2.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['cool-ip-api = cool_ip_api.main:cli']}

setup_kwargs = {
    'name': 'cool-ip-api',
    'version': '0.2.0',
    'description': 'A collections of wrapper for different IP info APIs',
    'long_description': '# cool-ip-api\n\n<a href="https://pypi.org/project/cool-ip-api/">\n    <img src="https://badge.fury.io/py/cool-ip-api.svg" alt="Package version">\n</a>\n\nA package to get information from multiple IP APIs about the clients IP or another requested IP.<br>\n\n## Installation\n**Requires python  3.10 and above.**\n```bash\npip install cool-ip-api\n```\n\n## Usage\n\n```python\n# Example with IPApiCom API\nfrom cool_ip_api.provider.ip_api_com import IPAPICom\n\nip_api_com = IPAPICom()\nip_api_com.resolve() # Returns a pydantic model with the data from the API\n```\n\n### Cli command\n\n```bash\ncool-ip-api\ncool-ip-api 1.1.1.1\n```\n\n## Supported APIs\n\n| Provider                                                              | Free plan available?                  | Rate limit   | Check   | IP Query |\n|-----------------------------------------------------------------------|---------------------------------------|--------------|---------|----------|\n| [abstractapi.com](https://www.abstractapi.com/api/ip-geolocation-api) | ✅                                     | 20.000/month | api-key | ✅        |\n| [ip-api.com](https://ip-api.com/)                                     | ✅                                     | 45/minute    | ip      | ✅        |\n| [ipwhois.io](https://ipwhois.io/)                                     | ✅                                     | 10.000/month | ip      | ✅        |\n| [ipapi.co](https://ipapi.co/)                                         | ✅                                     | 1.000/day    | ip      | ✅        |\n| [ipapi.com](https://ipapi.com/)                                       | ✅                                     | 1.000/month  | api-key | ✅        |\n| [ipify.org](https://www.ipify.org/)                                   | ✅                                     | None         | None    | ❌        |\n| [ipinfo.io](https://ipinfo.io/)                                       | ✅                                     | 50.000/month | api-key | ✅        |\n| [myip.wtf](https://myip.wtf/)                                         | ✅ ([Donate](https://myip.wtf/donate)) | 1/minute     | ip      | ❌        |\n\n## TODO\n\n- [ ] Add more providers\n    - [ ] [geo.ipify.org](https://geo.ipify.org/)\n- [ ] Add bulk query support for providers that support it\n- [ ] Add premium plan support for providers that support it\n- [ ] Add more tests\n    - [ ] Async tests\n    - [ ] Rate limit tests\n- [ ] Add more documentation',
    'author': 'sokripon',
    'author_email': 'sokripon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sokripon/cool-ip-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
