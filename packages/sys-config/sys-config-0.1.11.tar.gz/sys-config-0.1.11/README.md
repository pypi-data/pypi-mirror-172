# sys-config

<div align="center">

[![Build status](https://github.com/william-cass-wright/sys-config/workflows/build/badge.svg?branch=main&event=push)](https://github.com/william-cass-wright/sys-config/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/sys-config.svg)](https://pypi.org/project/sys-config/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/william-cass-wright/sys-config/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/william-cass-wright/sys-config/blob/main/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/william-cass-wright/sys-config/releases)
[![License](https://img.shields.io/github/license/william-cass-wright/sys-config)](https://github.com/william-cass-wright/sys-config/blob/main/LICENSE)
![Coverage Report](assets/images/coverage.svg)

</div>

`sys-config` is a Python package created with [william-cass-wright/cookiecutter-pypackage-slim](https://github.com/william-cass-wright/cookiecutter-pypackage-slim)... kinda

</div>

## Summary

## Usage

implementation example within [media-mgmt-cli]:

```python
from .config import ConfigHandler


class AwsStorageMgmt:
    def __init__(self):
        self.s3_resour = boto3.resource("s3")
        self.s3_client = boto3.client("s3")
        self.config = ConfigHandler(project_name="media_mgmt_cli")
        if self.config.check_config_exists():
            self.configs = self.config.get_configs()
            self.bucket = self.configs.get("aws_bucket", None)
            self.object_prefix = self.configs.get("aws_bucket_path", None)
        else:
            echo("config file does not exist, run `mmgmt configure`")

    def upload_file(self, file_name, object_name=None):
        """
        ...
        """
        echo(
            f"uploading: {file_name} \nto S3 bucket: {self.configs.get('aws_bucket')}/{self.configs.get('aws_bucket_path')}/{file_name}"
        )
        ...
```

## Future Work

- setup sys-config

## Project Examples

- [media-mgmt-cli]
- [secret-mgmt-cli]

[media-mgmt-cli]: https://github.com/william-cass-wright/media-mgmt-cli
[secret-mgmt-cli]: https://github.com/william-cass-wright/secrets-mgmt-cli
