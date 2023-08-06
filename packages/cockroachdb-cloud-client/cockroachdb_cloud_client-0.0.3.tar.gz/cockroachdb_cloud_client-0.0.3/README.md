# cockroachdb_cloud_client

A client library for accessing the CockroachDB Cloud API.

Read the [CockroachDB Cloud OpenAPI Spec](https://www.cockroachlabs.com/docs/api/cloud/v1.html) on our docs page.

## Usage

First, create a client, then, call your endpoint and use your models:

```python
from cockroachdb_cloud_client import AuthenticatedClient
from cockroachdb_cloud_client.models import ListClustersResponse
from cockroachdb_cloud_client.api.cockroach_cloud import cockroach_cloud_list_clusters
from cockroachdb_cloud_client.types import Response

import os

cc_key = os.environ['CC_KEY']

client = AuthenticatedClient(
    base_url="https://cockroachlabs.cloud",
    token=cc_key,
    headers={"cc-version": "2022-09-20"},
)

resp: Response[ListClustersResponse] = cockroach_cloud_list_clusters.sync_detailed(client=client)

for x in resp.parsed.clusters:
    print(x.name)

# Output:
# cute-otter
# gummy-rabbit
# half-weasel
# itchy-donkey
# redear-thrush
```

### Things to know

1. Every path/method combo becomes a Python module with four functions:
    1. `sync`: Blocking request that returns parsed data (if successful) or `None`
    2. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.
    3. `asyncio`: Like `sync` but async instead of blocking
    4. `asyncio_detailed`: Like `sync_detailed` but async instead of blocking

2. All path/query params, and bodies become method arguments.
3. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)
4. Any endpoint which did not have a tag will be in `cockroachdb_cloud_client.api.default`
