# Bitronit Python

Python Client for Bitronit (v2 API)


## Installation

The `bitronit` package is available on [PyPI](https://pypi.org/project/bitronit). Install with `pip`:

```bash
pip install bitronit
```


## Getting Started

The `BitronitClient` object can be created without authentication to make public requests. You can simply create Client object without any arguments.

For the private request the `BitronitClient` needs to be authenticated with api key and secret that you can create from API Management page in Bitronit dashboard. 


## Usage

After installing the library, just import the client.

```py
from bitronit.client import BitronitClient
```
You can use public endpoints without providing an api key/secret pair.

```py
my_client = BitronitClient()
my_client.get_assets()
```
If you have an api key/secret pair, you can use private endpoints

```py
my_client = BitronitClient(api_key='<Your Api Key>', api_secret='<Your Api Secret>')
my_client.get_wallets()
```