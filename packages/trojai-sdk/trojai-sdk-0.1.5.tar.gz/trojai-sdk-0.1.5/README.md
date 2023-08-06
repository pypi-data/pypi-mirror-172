# trojai-sdk

TrojAI's SDK and command line interface.

# SDK Components

## Client
```
from trojsdk import TrojClient
```

```
import json

##################################
keys = AOUSYDHLOAHUSLDIUHW

client = TrojClient()
client.set_credentials(
    id_token=keys["id_token"],
    refresh_token=keys["refresh_token"],
    api_key=keys["api_key"]    
)
```

## Config
```
from trojsdk import BaseTrojConfig
```

```

```