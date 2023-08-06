# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sys_config']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sys-config',
    'version': '0.1.11',
    'description': 'Awesome `sys-config` is a Python cli/package created with https://github.com/TezRomacH/python-package-template',
    'long_description': '# sys-config\n\n<div align="center">\n\n[![Build status](https://github.com/william-cass-wright/sys-config/workflows/build/badge.svg?branch=main&event=push)](https://github.com/william-cass-wright/sys-config/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/sys-config.svg)](https://pypi.org/project/sys-config/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/william-cass-wright/sys-config/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/william-cass-wright/sys-config/blob/main/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/william-cass-wright/sys-config/releases)\n[![License](https://img.shields.io/github/license/william-cass-wright/sys-config)](https://github.com/william-cass-wright/sys-config/blob/main/LICENSE)\n![Coverage Report](assets/images/coverage.svg)\n\n</div>\n\n`sys-config` is a Python package created with [william-cass-wright/cookiecutter-pypackage-slim](https://github.com/william-cass-wright/cookiecutter-pypackage-slim)... kinda\n\n</div>\n\n## Summary\n\n## Usage\n\nimplementation example within [media-mgmt-cli]:\n\n```python\nfrom .config import ConfigHandler\n\n\nclass AwsStorageMgmt:\n    def __init__(self):\n        self.s3_resour = boto3.resource("s3")\n        self.s3_client = boto3.client("s3")\n        self.config = ConfigHandler(project_name="media_mgmt_cli")\n        if self.config.check_config_exists():\n            self.configs = self.config.get_configs()\n            self.bucket = self.configs.get("aws_bucket", None)\n            self.object_prefix = self.configs.get("aws_bucket_path", None)\n        else:\n            echo("config file does not exist, run `mmgmt configure`")\n\n    def upload_file(self, file_name, object_name=None):\n        """\n        ...\n        """\n        echo(\n            f"uploading: {file_name} \\nto S3 bucket: {self.configs.get(\'aws_bucket\')}/{self.configs.get(\'aws_bucket_path\')}/{file_name}"\n        )\n        ...\n```\n\n## Future Work\n\n- setup sys-config\n\n## Project Examples\n\n- [media-mgmt-cli]\n- [secret-mgmt-cli]\n\n[media-mgmt-cli]: https://github.com/william-cass-wright/media-mgmt-cli\n[secret-mgmt-cli]: https://github.com/william-cass-wright/secrets-mgmt-cli\n',
    'author': 'sys-config',
    'author_email': 'hello@sys-config.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sys_config/sys-config',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
