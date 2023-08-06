Async package and CLI command for URL validation.

Allows you to check:
* server response code
* redirect settings
* presence of text on the page

It is possible to use throttling to avoid blocking.

# Install
```pip install py_url_validator```

# Usage

```python
import asyncio
from async_url_validator import StatusAssigner, DomainThrottler, URLValidator


async def main():
    status_assigner = StatusAssigner(page_text='not available')
    request_method = (status_assigner.page_text and 'GET') or 'HEAD'
    validator = URLValidator(request_method=request_method,
                             throttler=DomainThrottler(rate_limit_per_sec=10),
                             status_assigner=status_assigner)

    urls = ['https://www.python.org', 'http://google.com']
    async for status in validator.validate(*urls):
        print(status)


asyncio.run(main())
```


## CLI
```url_validator -i input.csv -o output.csv -s "not available"```