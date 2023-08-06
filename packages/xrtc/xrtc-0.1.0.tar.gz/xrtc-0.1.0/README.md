# XRTC API

This module is wrapper of XRTC API in Python. First, it incorporates usage of .env file to
load login and connection configurations. Second, it uses Pydantic to parse configurations,
serialized and deserialized request bodies and response data. Examples show discrete and
streaming use of the XRTC API.

## Installation

Installation from Pypi:
```
pip install xrtc
```

From source:
```
pip install .
```

## Login credentials and connection URLs

Login credentials are taken from the environment or from a .env file
(e.g. xrtc.env) placed to the work directory. Here is the format of
a sample file:
```
# XRTC credentials
ACCOUNT_ID=123
API_KEY=xxx

# Optionally, XRTC connection URLs if different from default
# LOGIN_URL = "https://api.xrtc.org/v1/auth/login"
# SET_URL = "https://api.xrtc.org/v1/item/set"
# GET_URL = "https://api.xrtc.org/v1/item/get"
```

## Usage examples

See examples directory in GitHub.

Simple set and get:

```
from xrtc import *

with XRTC(env_file_credentials="xrtc_dev.env") as xrtc:
    # Upload data
    xrtc.set_item(items=[{"portalid": "send", "payload": "sample"}])

    # Download data and parse it
    print(xrtc.get_item(portals=[{"portalid": "send"}]).dict())
```
