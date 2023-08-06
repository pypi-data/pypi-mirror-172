# SearchUnify SDK

## Overview
The SearchUnify SDK for Python enabled developers to easily work with the SearchUnify platform and build scalable solutions with search, analytics, crawlers and more. You can get started in minutes using PyPI or by downloading the tar file.
The SearchUnify SDK for simpliﬁes use of SearchUnify Services by providing a set of libraries that are consistent and familiar for Python developers. It provides support for API lifecycle consideration such as credential management, retries, data marshaling, and serialization. The SearchUnify SDK for Python also supports higher level abstractions for simplified development.

## Key Features
* HTTP/2 Support and pluggable HTTP layer, new programming interfaces seamlessly take advantage of HTTP/2 features and provide new ways to build applications.
* Nonblocking I/O, the SearchUnify SDK utilizes a new, nonblocking SDK architecture to support true nonblocking I/O. It features truly non blocking asynchronous clients that implement high concurrency across a few threads.

## Getting Started
Sign up for SearchUnify, before you begin, you need a SearchUnify account. Please see the oAuth section of the developer guide for information about how to retrieve your SearchUnify credentials.

## Installation
SDK requires Python 3+ and pip to run.
The recommended way to use the SearchUnify SDK for Python in your project is to consume it from PyPI.
```python
pip install su-sdk
```
## Execution
Initiate SearchUnify Python SDK on Server. Using the SDK, you can route search requests. To start using, initialize the SDK with your URL and API key.
```python
from searchunify import Searchunify

username = "changeme"
password = "changeme"
clientId = "changeme"
secrets = "changeme"
instance = "changeme"

client =  Searchunify(instance=instance, username=username, password=password, client_id=clientId, client_secret=secrets)

startDate       =   "changeme"
endDate         =   "changeme"
searchClientId  =   "changeme"
data          =   client.get_tiles_data(startDate=startDate, endDate=endDate, searchClientId=searchClientId)
print("The tile data response: ", data)
```
The access token will expire after 4 hours and you need to refresh that.

```python
result = client.refresh_token()
```
## Documentation
Please refer to the SearchUnify developer guide to use the SDK. https://docs.searchunify.com/Content/Developer-Guides/SDKs-Python.htm

The documentation is in review and might contain bugs🐞, we will update the link on https://docs.searchunify.com once its's final.


## License

MIT

**&copy; Powered by [SearchUnify](https://www.searchunify.com/)!**