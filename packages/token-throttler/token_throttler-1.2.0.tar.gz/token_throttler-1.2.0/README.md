# Token throttler

![Coverage](https://img.shields.io/gitlab/coverage/vojko.pribudic/token-throttler/main?job_name=tests)
![Version](https://img.shields.io/pypi/pyversions/token-throttler)
![Downloads](https://pepy.tech/badge/token-throttler)
![Formatter](https://img.shields.io/badge/code%20style-black-black)
![License](https://img.shields.io/pypi/l/token-throttler)

**Token throttler** is an extendable rate-limiting library somewhat based on a [token bucket algorithm](https://en.wikipedia.org/wiki/Token_bucket).

## Table of contents

1. [ Installation ](#installation)
2. [ Features ](#features)
3. [ Usage ](#usage)
    1. [ Manual usage example ](#usage-manual)
    2. [ Decorator usage example ](#usage-decorator)
4. [ Storage ](#storage)
5. [ Configuration ](#configuration)
   1. [ Configuration usage ](#configuration-usage)

<a name="installation"></a>
## 1. Installation

Token throttler is available on PyPI:
```console 
$ python -m pip install token-throttler
```
Token throttler officially supports Python >= 3.7.

*NOTE*: Depending on the storage engine you pick, you can install token throttler with extras:
```console 
$ python -m pip install token-throttler[redis]
$ python -m pip install token-throttler[aioredis]
```

<a name="features"></a>
## 2. Features

- Blocking (TokenThrottler) and non-blocking (TokenThrottlerAsync)
- Global throttler(s) configuration
- Configurable token throttler cost and identifier
- Multiple buckets per throttler per identifier
- Buckets can be added/removed manually or by a `dict` configuration
- Manual usage or usage via decorator
- Decorator usage supports async code too
- Custom decorator can be written
- Extendable storage engine (eg. Redis)

<a name="usage"></a>
## 3. Usage

Token throttler supports both manual usage and via decorator.

Decorator usage supports both async and sync.

<a name="usage-manual"></a>
### 1) Manual usage example:

```python
from token_throttler import TokenBucket, TokenThrottler
from token_throttler.storage import RuntimeStorage

throttler: TokenThrottler = TokenThrottler(cost=1, storage=RuntimeStorage())
throttler.add_bucket(identifier="hello_world", bucket=TokenBucket(replenish_time=10, max_tokens=10))
throttler.add_bucket(identifier="hello_world", bucket=TokenBucket(replenish_time=30, max_tokens=20))


def hello_world() -> None:
    print("Hello World")


for i in range(10):
    throttler.consume(identifier="hello_world")
    hello_world()

if throttler.consume(identifier="hello_world"):
    hello_world()
else:
    print("bucket_one ran out of tokens")
```

<a name="usage-decorator"></a>
### 2) Decorator usage example:

```python
from token_throttler import TokenBucket, TokenThrottler, TokenThrottlerException
from token_throttler.storage import RuntimeStorage

throttler: TokenThrottler = TokenThrottler(1, RuntimeStorage())
throttler.add_bucket("hello_world", TokenBucket(10, 10))
throttler.add_bucket("hello_world", TokenBucket(30, 20))


@throttler.enable("hello_world")
def hello_world() -> None:
    print("Hello World")


for i in range(10):
    hello_world()

try:
    hello_world()
except TokenThrottlerException:
    print("bucket_one ran out of tokens")
```

For other examples see [**examples**](https://gitlab.com/vojko.pribudic/token-throttler/-/tree/main/examples) directory.

<a name="storage"></a>
## 4. Storage

`TokenThrottler` supports `RuntimeStorage` and `RedisStorage`.
`TokenThrottlerAsync` supports `RedisStorageAsync`

If you want your own storage engine, feel free to extend the `token_throttler.storage.BucketStorage` or `token_throttler.storage.BucketStorageAsync` classes.

For storage examples see [**examples**](https://gitlab.com/vojko.pribudic/token-throttler/-/tree/main/examples) directory.

<a name="configuration"></a>
## 5. Configuration

Token throttler supports global configuration by making use of `ThrottlerConfig` class.

Configuration params:
- `IDENTIFIER_FAIL_SAFE` - if invalid identifier is given as a param for the `consume` method and `IDENTIFIER_FAIL_SAFE`
is set to `True`, no `KeyError` exception will be raised and `consume` will act like a limitless bucket is being consumed.
- `ENABLE_THREAD_LOCK` - if set to `True`, throttler will acquire a thread lock upon calling `consume` method and release
the lock once the `consume` is finished. This avoids various race conditions at a slight performance cost.

<a name="configuration-usage"></a>
### Configuration usage

```python
from token_throttler import ThrottlerConfig, TokenBucket, TokenThrottler
from token_throttler.storage import RuntimeStorage

ThrottlerConfig.set({
   "ENABLE_THREAD_LOCK": False,
   "IDENTIFIER_FAIL_SAFE": True,
})
throttler: TokenThrottler = TokenThrottler(1, RuntimeStorage())
throttler.add_bucket("hello_world", TokenBucket(10, 10))
throttler.add_bucket("hello_world", TokenBucket(30, 20))
...
```
