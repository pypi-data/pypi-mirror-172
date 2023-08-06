# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sandclock']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sandclock',
    'version': '0.1.3',
    'description': 'A decorator for examining the execution time of asynchronous/synonymous function.',
    'long_description': '##### Basic Usage\nA decorator for measuring asynchronous/synchronous function execution time (in seconds) is offered by this Python module.\n- 1st parameter: total number of iterations of the function. defaults to 1.\n- 2nd parameter: (int, optional): precision of execution time in seconds. defaults to 5.\n- 3rd parameter: (bool, optional): whether each function execution time is printed. defaults to true.\n\n##### Example 1: synonymous function\n```python\nfrom sandclock import sandclock\n@sandclock(3) #execute f1() 3 times.\ndef f1(x):\n    print("f1: ", x)\n\nf1("hello world")\n\n```\nResults:\n```\nSandclock: synchronous <function f1 at 0x7f89eaca7e50> with args (\'hello world\',) {}\nSandclock: iteration: 0 started, <function f1 at 0x7f89eaca7e50> with args (\'hello world\',) {}\nf1:  hello world\nSandclock: iteration: 0 finished, <function f1 at 0x7f89eaca7e50> in 0.000823 second(s)\nSandclock: iteration: 1 started, <function f1 at 0x7f89eaca7e50> with args (\'hello world\',) {}\nf1:  hello world\nSandclock: iteration: 1 finished, <function f1 at 0x7f89eaca7e50> in 0.000075 second(s)\nSandclock: iteration: 2 started, <function f1 at 0x7f89eaca7e50> with args (\'hello world\',) {}\nf1:  hello world\nSandclock: iteration: 2 finished, <function f1 at 0x7f89eaca7e50> in 0.000151 second(s)\nSandclock: total time: 0.001050, total iterations: 3```\n```\n##### Example 2: (Asynchronous function)\n```python\nimport aiohttp\nimport asyncio\nfrom sandclock import sandclock\n\n\nasync def status(session: aiohttp.ClientSession, url: str) -> int:\n    async with session.get(url) as result:\n        return result.status\n\n#execute f2() 2 times, 3 precisions, printing details of each function call.\n@sandclock(2, 3, True)\nasync def f2():\n    async with aiohttp.ClientSession() as session:\n        urls = [\'https://google.com\', \'xxx://bad-request.com\']\n        tasks = [status(session, url) for url in urls]\n        results = await asyncio.gather(*tasks, return_exceptions=True)\n\n        exceptions = [res for res in results if isinstance(res, Exception)]\n        successful_results = [res for res in results if not isinstance(res, Exception)]\n\n        print(f\'All results: {results}\')\n        print(f\'Finished successfully: {successful_results}\')\n        print(f\'Threw exceptions: {exceptions}\')\n\nasyncio.run(f2())\n```\nResults:\n```\nSandclock: coroutine <function f2 at 0x7f632fd3e430> with args () {}\nSandclock: iteration: 0 started, <function f2 at 0x7f632fd3e430> with args () {}\nAll results: [200, AssertionError()]\nFinished successfully: [200]\nThrew exceptions: [AssertionError()]\nSandclock: iteration: 0 finished, <function f2 at 0x7f632fd3e430> in 2.400 second(s)\nSandclock: iteration: 1 started, <function f2 at 0x7f632fd3e430> with args () {}\nAll results: [200, AssertionError()]\nFinished successfully: [200]\nThrew exceptions: [AssertionError()]\nSandclock: iteration: 1 finished, <function f2 at 0x7f632fd3e430> in 2.385 second(s)\nSandclock: total time: 4.785 second(s), total iterations: 2\n```\n',
    'author': 'fadedreams7',
    'author_email': 'fadedreams7@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
