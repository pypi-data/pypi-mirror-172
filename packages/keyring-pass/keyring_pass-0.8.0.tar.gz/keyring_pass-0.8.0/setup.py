# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keyring_pass']

package_data = \
{'': ['*']}

install_requires = \
['jaraco-classes>=3.2.3,<4.0.0', 'keyring>=23.9.3,<24.0.0']

entry_points = \
{'keyring.backends': ['pass = keyring_pass']}

setup_kwargs = {
    'name': 'keyring-pass',
    'version': '0.8.0',
    'description': 'https://www.passwordstore.org/ backend for https://pypi.org/project/keyring/',
    'long_description': '# keyring_pass\n\nThis is a [`pass`](https://www.passwordstore.org/) backend for [`keyring`](https://pypi.org/project/keyring/)\n\nInstall with `pip install keyring-pass` and set the following content in\nyour [`keyringrc.cfg`](https://pypi.org/project/keyring/#config-file-path) file:\n\n```ini\n[backend]\ndefault-keyring = keyring_pass.PasswordStoreBackend\n```\n\nYou can modify the default `python-keyring` prefix for `pass`, by:\n\n- adding following to `keyringrc.cfg`:\n\n    ```ini\n    [pass]\n    key-prefix=alternative/prefix/path\n    binary=gopass\n    ```\n\n- (for `keyring` version 23.0.0 or higher) setting environment variables:\n    - `KEYRING_PROPERTY_PASS_KEY_PREFIX`\n    - `KEYRING_PROPERTY_PASS_BINARY`\n\n- You can clear the path (start from root), by setting above to `.` or an empty value (just `key-prefix=` on the line).\n\n## Test your setup\n\nYou can check if your setup works end-to-end (creates, reads and deletes a key from password store).\n\n```shell\n# warning: this will create and delete a key at `<prefix>/test/asd` in your password store\npython -m keyring_pass\n```\n',
    'author': 'Krzysztof Nazarewski',
    'author_email': '3494992+nazarewk@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nazarewk/keyring_pass',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
