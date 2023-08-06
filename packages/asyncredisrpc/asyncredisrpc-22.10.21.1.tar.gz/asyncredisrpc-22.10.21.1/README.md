# asyncredisrpc
A naive async rpc framework based on redis, written in Python.

asyncredisrpc is inspired by https://github.com/gowhari/pyredisrpc.

# Installation

```shell
pip install asyncredisrpc
```

# Usage

## server

```python
import asyncio
from asyncredisrpc.server import AsyncServer

queue_name = 'test_queue'
server = AsyncServer(queue_name, '172.21.16.114')


@server.task
async def sum(x, y):
    print('summing...')
    await asyncio.sleep(1)
    return x + y


if __name__ == '__main__':
    asyncio.run(server.run())
```

## client

```python
import asyncio
from asyncredisrpc.client import AsyncClient


async def main():
    queue_name = 'test_queue'
    client = AsyncClient(queue_name, '172.21.16.114')
    await client.connect()
    ret, data = await client.call('sum', 14, 3)
    print(f'get result: {ret} {data}')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
```