# Async IPFS API

## Install

```bash
pip install asyncipfscluster
```

## Usage

```python
import asyncio
from asyncipfscluster import IPFSClient

client = IPFSClient("http://127.0.0.1:9094")

async def main():
    async with client as session:
        cid = await client.add_bytes(b"Hello from cofob!", "text/plain")
        print(cid)

asyncio.run(main())
```
