<div id="top"></div>

<p align="center">
    <a href="https://github.com/libninjacom/postman-py/graphs/contributors">
        <img src="https://img.shields.io/github/contributors/libninjacom/postman-py.svg?style=flat-square" alt="GitHub Contributors" />
    </a>
    <a href="https://github.com/libninjacom/postman-py/stargazers">
        <img src="https://img.shields.io/github/stars/libninjacom/postman-py.svg?style=flat-square" alt="Stars" />
    </a>
    <a href="https://github.com/libninjacom/postman-py/actions">
        <img src="https://img.shields.io/github/workflow/status/libninjacom/postman-py/CI?style=flat-square" alt="Build Status" />
    </a>
    
<a href="https://pypi.org/project/postman_api">
    <img src="https://img.shields.io/pypi/dm/postman_api?style=flat-square" alt="Downloads" />
</a>

<a href="https://pypi.org/project/postman_api">
    <img src="https://img.shields.io/pypi/v/postman_api?style=flat-square" alt="Pypi" />
</a>

</p>

Postman client, generated from the OpenAPI spec.

# Usage

```python
import os
from postman_api import AsyncPostmanClient
from postman_api import PostmanClient

def main():
    client = PostmanClient.from_env()
    response = client.get_all_apis()
    print(f"{response!r}")

async def async_main():
    client = AsyncPostmanClient.from_env()
    response = await client.get_all_apis()
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio
        asyncio.run(async_main())
    else:
        main()


```

This example loads configuration from environment variables, specifically:

* `POSTMAN_API_KEY`





# Documentation


* [API Documentation](https://www.postman.com/postman/workspace/postman-public-workspace/documentation/12959542-c8142d51-e97c-46b6-bd77-52bb66712c9a)



You can see working examples of every API call in the `examples/` directory.

# Contributing

Contributions are welcome!

*Library created with [Libninja](https://www.libninja.com).*