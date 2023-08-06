'''
# replace this

## Getting Started

### TypeScript

#### Installation

```shell
$ npm install cdk-extensions
```

### Python

#### Installation

```shell
$ pip install cdk-extensions
```

### Examples

#### AwsLoggingStack

Minimal deployable example creates the default logging strategy defined in AwsLoggingStack for Elastic Load Balancer, CloudFront, CloudTrail, VPC Flow Logs, S3 access logs, SES logs, and WAF logs. For each service, an S3 bucket is created and a Glue crawler to analyze and categorize the data and store the associated metadata in the AWS Glue Data Catalog. Default named queries have been defined for each AWS service. For more details on this and the other available stacks and constructs, consult the respective READMEs.

**TypeScript**

```TypeScript
import { AwsLoggingStack } from 'cdk-extensions/stacks';
```

```TypeScript
new AwsLoggingStack(this, 'AwsLoggingStack')
```

**Python**

```Python
from cdk_extensions.stacks import (
  AwsLoggingStack
)
```

```Python
aws_logging_stack = AwsLoggingStack(self, 'AwsLoggingStack')
```

#### Deploy

```shell
$ cdk deploy
```

#### FourTierNetwork

// To Do
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

__all__ = [
    "athena",
    "ec2",
    "glue",
    "glue_tables",
    "kinesis_firehose",
    "ram",
    "s3_buckets",
    "sso",
    "stacks",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import athena
from . import ec2
from . import glue
from . import glue_tables
from . import kinesis_firehose
from . import ram
from . import s3_buckets
from . import sso
from . import stacks
