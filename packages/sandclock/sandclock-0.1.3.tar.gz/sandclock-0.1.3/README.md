##### Basic Usage
A decorator for measuring asynchronous/synchronous function execution time (in seconds) is offered by this Python module.
- 1st parameter: total number of iterations of the function. defaults to 1.
- 2nd parameter: (int, optional): precision of execution time in seconds. defaults to 5.
- 3rd parameter: (bool, optional): whether each function execution time is printed. defaults to true.

##### Example 1: synonymous function
```python
from sandclock import sandclock
@sandclock(3) #execute f1() 3 times.
def f1(x):
    print("f1: ", x)

f1("hello world")

```
Results:
```
Sandclock: synchronous <function f1 at 0x7f89eaca7e50> with args ('hello world',) {}
Sandclock: iteration: 0 started, <function f1 at 0x7f89eaca7e50> with args ('hello world',) {}
f1:  hello world
Sandclock: iteration: 0 finished, <function f1 at 0x7f89eaca7e50> in 0.000823 second(s)
Sandclock: iteration: 1 started, <function f1 at 0x7f89eaca7e50> with args ('hello world',) {}
f1:  hello world
Sandclock: iteration: 1 finished, <function f1 at 0x7f89eaca7e50> in 0.000075 second(s)
Sandclock: iteration: 2 started, <function f1 at 0x7f89eaca7e50> with args ('hello world',) {}
f1:  hello world
Sandclock: iteration: 2 finished, <function f1 at 0x7f89eaca7e50> in 0.000151 second(s)
Sandclock: total time: 0.001050, total iterations: 3```
```
##### Example 2: (Asynchronous function)
```python
import aiohttp
import asyncio
from sandclock import sandclock


async def status(session: aiohttp.ClientSession, url: str) -> int:
    async with session.get(url) as result:
        return result.status

#execute f2() 2 times, 3 precisions, printing details of each function call.
@sandclock(2, 3, True)
async def f2():
    async with aiohttp.ClientSession() as session:
        urls = ['https://google.com', 'xxx://bad-request.com']
        tasks = [status(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        exceptions = [res for res in results if isinstance(res, Exception)]
        successful_results = [res for res in results if not isinstance(res, Exception)]

        print(f'All results: {results}')
        print(f'Finished successfully: {successful_results}')
        print(f'Threw exceptions: {exceptions}')

asyncio.run(f2())
```
Results:
```
Sandclock: coroutine <function f2 at 0x7f632fd3e430> with args () {}
Sandclock: iteration: 0 started, <function f2 at 0x7f632fd3e430> with args () {}
All results: [200, AssertionError()]
Finished successfully: [200]
Threw exceptions: [AssertionError()]
Sandclock: iteration: 0 finished, <function f2 at 0x7f632fd3e430> in 2.400 second(s)
Sandclock: iteration: 1 started, <function f2 at 0x7f632fd3e430> with args () {}
All results: [200, AssertionError()]
Finished successfully: [200]
Threw exceptions: [AssertionError()]
Sandclock: iteration: 1 finished, <function f2 at 0x7f632fd3e430> in 2.385 second(s)
Sandclock: total time: 4.785 second(s), total iterations: 2
```
