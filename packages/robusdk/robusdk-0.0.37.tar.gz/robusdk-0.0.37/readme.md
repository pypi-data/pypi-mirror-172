```js
(async () => {
  const robsdk = require('robusdk')
  const {Coroutine, Sequence, Logger, Awaitable} = require('robusdk')

  const Client = robsdk({
    url: 'http://localhost/',
    username: 'username',
    password: 'password'
  })

  const rpc = Client('rpc')
  const pipeline = Client('pipeline')
  Logger.info(await new Coroutine([
    new Sequence(() => rpc.methodA(...paramsA), Logger.debug, Logger.error),
    new Sequence(() => rpc.methodB(...paramsB), Logger.debug, Logger.error),
    new Sequence(() => pipeline.methodA(), Logger.debug, Logger.error),
    new Sequence(() => pipeline.methodB(), Logger.debug, Logger.error),
    new Awaitable(() => pipeline([methodA, methodB]), Logger.debug),
  ]))
})()
```

```python
async def future():
  from robusdk import robusdk, Logger, Sequence, Coroutine, Awaitable
  Client = robsdk(
    url='http://localhost/',
    username='username',
    password='password',
  )
  rpc = Client('rpc')
  pipeline = Client('pipeline')
  Logger.info(await Coroutine([
      Sequence(lambda: rpc.methodA(**paramsA), Logger.debug, Logger.error),
      Sequence(lambda: rpc.methodB(**paramsB), Logger.debug, Logger.error),
      Sequence(lambda: pipeline.methodA(), Logger.debug, Logger.error),
      Sequence(lambda: pipeline.methodB(), Logger.debug, Logger.error),
      Awaitable(lambda: pipeline([methodA, methodB]), Logger.debug),
  ]))

from asyncio import run
run(future())
```
