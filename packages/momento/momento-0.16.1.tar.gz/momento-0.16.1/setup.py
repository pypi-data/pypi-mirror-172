# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['momento',
 'momento._utilities',
 'momento.aio',
 'momento.incubating',
 'momento.incubating._utilities',
 'momento.incubating.aio']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT[crypto]==2.4.0', 'grpcio==1.50.0', 'momento-wire-types==0.31.1']

setup_kwargs = {
    'name': 'momento',
    'version': '0.16.1',
    'description': 'SDK for Momento',
    'long_description': '# Momento client-sdk-python\n\n:warning: Experimental SDK :warning:\n\nPython SDK for Momento is experimental and under active development.\nThere could be non-backward compatible changes or removal in the future.\nPlease be aware that you may need to update your source code with the current version of the SDK when its version gets upgraded.\n\n---\n\n<br/>\n\nPython SDK for Momento, a serverless cache that automatically scales without any of the operational overhead required by traditional caching solutions.\n\n<br/>\n\n## Getting Started :running:\n\n### Requirements\n\n- [Python 3.7](https://www.python.org/downloads/) or above is required\n- A Momento Auth Token is required, you can generate one using the [Momento CLI](https://github.com/momentohq/momento-cli)\n\n<br/>\n\n### Installing Momento and Running the Example\n\nCheck out our [Python SDK example](/examples/)!\n\n<br/>\n\n### Using Momento\n\n```python\nimport os\nimport momento.simple_cache_client as simple_cache_client\n\n# Initializing Momento\n_MOMENTO_AUTH_TOKEN = os.getenv(\'MOMENTO_AUTH_TOKEN\')\n_ITEM_DEFAULT_TTL_SECONDS = 60\nsimple_cache_client.init(_MOMENTO_AUTH_TOKEN, _ITEM_DEFAULT_TTL_SECONDS) as cache_client\n\n# Creating a cache named "cache"\n_CACHE_NAME = \'cache\'\ncache_client.create_cache(_CACHE_NAME)\n\n# Sets key with default TTL and get value with that key\n_KEY = \'MyKey\'\n_VALUE = \'MyValue\'\ncache_client.set(_CACHE_NAME, _KEY, _VALUE)\nget_resp = cache_client.get(_CACHE_NAME, _KEY)\nprint(f\'Looked up Value: {str(get_resp.value())}\')\n\n# Sets key with TTL of 5 seconds\ncache_client.set(_CACHE_NAME, _KEY, _VALUE, 5)\n\n# Permanently deletes cache\ncache_client.delete_cache(_CACHE_NAME)\n```\n\n<br/>\n',
    'author': 'Momento',
    'author_email': 'hello@momentohq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gomomento.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
