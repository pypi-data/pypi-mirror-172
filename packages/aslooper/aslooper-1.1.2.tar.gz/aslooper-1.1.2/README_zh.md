# aslooper (佛跳墙活套)

> looper
> 用来捕获 SIGINT, SIGTERM 信号后取消所有运行任务。
> 支持执行自定义的调用。
> 退出运行不引入asyncio cancelled报错。

## 使用aslooper

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

## 带参数使用aslooper

```python
import asyncio
from aslooper import looper


async def run(i):
    while True:
        print(f"{i} running.")
        await asyncio.sleep(1)


def some_call():
    print("some_call")


# looper的call参数同时支持同步或异步的可调用对象。
@looper(some_call)
async def main():
    while True:
        print("run something.")
        await asyncio.sleep(1)


asyncio.run(main())
```