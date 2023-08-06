# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fraudrecord', 'fraudrecord.query', 'fraudrecord.query_aio']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10,<2.0']

extras_require = \
{'aio': ['aiohttp>=3.8,<4.0']}

entry_points = \
{'console_scripts': ['fraudrecord-query = fraudrecord.query.cli:main']}

setup_kwargs = {
    'name': 'fraudrecord',
    'version': '2022.10.22',
    'description': 'FraudRecord API client',
    'long_description': '# FraudRecord API client for Python\n\nInstall from PyPI:\n\n```sh\n$ pip install fraudrecord\n```\n\nIf you will use the non-blocking API, include `aio` extra:\n```sh\n$ pip install fraudrecord[aio]\n```\n\nThis package is maintained, stable, and perpetually tested. There will never be\nany breaking changes.\n\n## Example\n\nUsing the blocking API:\n\n```python\nfrom fraudrecord.query import query as fraudrecord_query\n\nif __name__ == "__main__":\n    api_code = "a51ff508c331b7e9" # XXX: use your own\n    print(fraudrecord_query(api_code, email="example@example.org"))\n```\n\nUsing the non-blocking API:\n\n```python\nimport asyncio\n\nfrom fraudrecord.query_aio import query as fraudrecord_query\n\n\nasync def main():\n    api_code = "a51ff508c331b7e9" # XXX: use your own\n    response = await fraudrecord_query(api_code, email="example@example.org")\n    print(response)\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\nUsing the CLI:\n\n```sh\n$ FRAUDRECORD_API_CODE=a51ff508c331b7e9 fraudrecord-query --email=example@example.org\n```\n\n## Documentation\n\n### `fraudrecord.hash`\n\nFraudRecord hashing scheme as described on <https://fraudrecord.com/security/>.\n\n32,000 iterations of SHA-1. Case- and whitespace- insensitive: the input is\nlowercased and stripped of all whitespace. The hexadecimal digest of each\niteration is fed into the next iteration. The input of each iteration\nis prefixed with `fraudrecord-`.\n\n- function `hexdigest(s: str) -> str`\n\n  Returns the hexadecimal digest of the input string.\n\n### `fraudrecord.model`\n\nConcepts of FraudRecord API.\n\n- type `APICode`\n\n  API code. Lowercase alphanumeric string, 16 characters. Get one by signing up\n  with FraudRecord and creating a reporter profile.\n\n- type `Reliability`\n\n  Result reliability measurement. Decimal; either 0.0 (if there are no submitted\n  reports) or between 1.0 and 10.0 with one digit after the decimal point.\n\n- type `ReportCode`\n\n  Report code. Lowercase alphanumeric string, 16 characters. Used in order to\n  fetch a human-readable report.\n\n- constant `ENDPOINT: HttpUrl`\n\n  API endpoint URL.\n\n- function `query_url(api_code: APICode, **data_vars: str) -> HttpUrl`\n\n  Given an API code and non-hashed data variables, returns the corresponding\n  query API URL.\n\n  Data variables are arbitrary bits of information about someone as described\n  on <https://fraudrecord.com/developers/> under "Data variables". Well-known\n  data variable names are:\n  + `name`: full name\n  + `company`: company name\n  + `email`: email address\n  + `address`: postal address\n  + `phone`: phone number\n  + `ip`: registration IP address\n  + `hostname`: server hostname\n  + `accountuser`: hosting account username\n  + `accountpass`: hosting account password\n  + `domain`: domain name without `www.`\n  + `paypalemail`: PayPal email address\n  + `ccname`: name on the credit card\n  + `ccnumber`: credit card number\n\n- function `report_url(report_code: ReportCode) -> HttpUrl`\n\n  Given a report code, returns the corresponding human-readable report URL.\n\n- class `QueryResponse`\n\n  Query API response.\n\n  + field `value: NonNegativeInt`\n\n    Total sum of points (severity scores) across all submitted reports.\n\n  + field `total_reports: NonNegativeInt`\n\n    Total number of the submitted reports.\n\n  + field `reliability: Reliability`\n\n    Result reliability measurement, out of possible 10.\n\n  + field `report_url: HttpUrl`\n\n    Human-readable report URL.\n\n    Example: https://www.fraudrecord.com/api/?showreport=0f5dac5aab7762e6\n\n  + class method `parse(s: str) -> QueryResponse`\n\n    Parses the input string containing the query API HTTP response body\n    into a `QueryResponse` object.\n\n### `fraudrecord.query`\n\nBlocking FraudRecord query API client.\n\n- function `query(api_code: APICode, **data_vars: str) -> QueryResponse`\n\n  Makes a query request to the API and returns a `QueryResponse`.\n\n### `fraudrecord.query.cli`\n\nFraudRecord query API command-line interface.\n\nUsage: `fraudrecord-query --DATA_VARIABLE=VALUE ...`\n\n`FRAUDRECORD_API_CODE` environment variable must be set to a valid FraudRecord\nAPI code. Get one by signing up with FraudRecord and creating a reporter profile.\n\n### `fraudrecord.query_aio`\n\nNon-blocking FraudRecord query API client.\n\n*Requires `aio` extra to be installed.*\n\n- async function `query(api_code: APICode, **data_vars: str) -> QueryResponse`\n\n  Makes a query request to the API and returns a `QueryResponse`.\n\n---\n\nNote that the report submission functionality isn\'t and won\'t be implemented.\nI believe that users of FraudRecord violate their clients\' privacy, and I don\'t\nwant to be a part of that.\n\nWhile it\'s true that FraudRecord only stores hashes of (arbitrary, sensitive)\ndata, if you do end up in the database, it lets anyone on the internet easily\ncheck if their guess of your personal email address, physical address, legal\nname, credit card number, IP address, and such is correct or not as long as\nthey know any single one of these bits of information in advance. There is\nno defined limit to the number of guesses they could make.\n\nMoreover, reports themselves are presented in cleartext and frequently contain\nsome sensitive data anyway. Here you can see various FraudRecord users posting\ntheir (ostensibly fraudulent) clients\' full names, addresses, and even, in one\ncase, a photo of the driver\'s license: [\\[1\\]][1], [\\[2\\]][2], [\\[3\\]][3].\nI wish I was making it up.\n\n[1]: https://web.archive.org/web/20221020093115/https://www.fraudrecord.com/api/?showreport=f0e0e7544b149849\n[2]: https://web.archive.org/web/20221020093328/https://www.fraudrecord.com/api/?showreport=f17ed61cb427f320\n[3]: https://web.archive.org/web/20221020094049/https://www.fraudrecord.com/api/?showreport=66853df490a28d3d\n\nThis API client is intended for privacy research only.\n',
    'author': 'Yana Luna-Terra',
    'author_email': 'yana@riseup.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/yanalunaterra/fraudrecord-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
