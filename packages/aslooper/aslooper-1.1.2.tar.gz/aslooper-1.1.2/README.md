# aslooper

> looper
> Used to cancel all running tasks after catching SIGINT, SIGTERM signals,
> Quit running without raise asyncio cancelled error.

## use looper

```python
import asyncio
from aslooper import looper


async def run(i):
    while True:
        print(f"{i} running.")
        await asyncio.sleep(1)


@looper()
async def main():
    tasks = [run(i) for i in range(3)]
    await asyncio.gather(*tasks)


asyncio.run(main())
```

## run with a call

```python
import asyncio
from aslooper import looper


async def run(i):
    while True:
        print(f"{i} running.")
        await asyncio.sleep(1)


def some_call():
    print("some_call")


@looper(some_call)
async def main():
    while True:
        print("run something.")
        await asyncio.sleep(1)


asyncio.run(main())
```