# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_simple_security']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.70', 'urllib3>=1.26.12']

setup_kwargs = {
    'name': 'fastapi-simple-security',
    'version': '1.2',
    'description': 'API key-based security for FastAPI',
    'long_description': '# FastAPI simple security\n\n[![codecov](https://codecov.io/github/mrtolkien/fastapi_simple_security/branch/master/graph/badge.svg?token=8VIKJ9J3XF)](https://codecov.io/github/mrtolkien/fastapi_simple_security)\n[![Python Tests](https://github.com/mrtolkien/fastapi_simple_security/actions/workflows/pr_python_tests.yml/badge.svg)](https://github.com/mrtolkien/fastapi_simple_security/actions/workflows/pr_python_tests.yml)\n[![Linting](https://github.com/mrtolkien/fastapi_simple_security/actions/workflows/push_sanity_check.yml/badge.svg)](https://github.com/mrtolkien/fastapi_simple_security/actions/workflows/push_sanity_check.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit enabled][pre-commit badge]][pre-commit project]\n\n[pre-commit badge]: <https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white>\n[pre-commit project]: <https://pre-commit.com/>\n\nAPI key based security package for FastAPI, focused on simplicity of use:\n\n- Full functionality out of the box, no configuration required\n- API key security with local `sqlite` backend, working with both header and query parameters\n- Default 15 days deprecation for generated API keys\n- Key creation, revocation, renewing, and usage logs handled through administrator endpoints\n- No dependencies, only requiring `FastAPI` and the python standard library\n\nThis module cannot be used for any kind of distributed deployment. It\'s goal is to help have some basic security features\nfor simple one-server API deployments, mostly during development.\n\n## Installation\n\n`pip install fastapi_simple_security`\n\n### Usage\n\n### Creating an application\n\n```python\nfrom fastapi_simple_security import api_key_router, api_key_security\nfrom fastapi import Depends, FastAPI\n\napp = FastAPI()\n\napp.include_router(api_key_router, prefix="/auth", tags=["_auth"])\n\n@app.get("/secure", dependencies=[Depends(api_key_security)])\nasync def secure_endpoint():\n    return {"message": "This is a secure endpoint"}\n```\n\nResulting app is:\n\n![app](images/auth_endpoints.png)\n\n### API key creation through docs\n\nStart your API and check the logs for the automatically generated secret key if you did not provide one through\nenvironment variables.\n\n![secret](images/secret.png)\n\nGo to `/docs` on your API and inform this secret key in the `Authorize/Secret header` box.\nAll the administrator endpoints only support header security to make sure the secret key is not inadvertently\nshared when sharing an URL.\n\n![secret_header](images/secret_header.png)\n\nThen, you can use `/auth/new` to generate a new API key.\n\n![api key](images/new_api_key.png)\n\nAnd finally, you can use this API key to access the secure endpoint.\n\n![secure endpoint](images/secure_endpoint.png)\n\n### API key creation in python\n\nYou can of course automate API key acquisition through python with `requests` and directly querying the endpoints.\n\nIf you do so, you can hide the endpoints from your API documentation with the environment variable\n`FASTAPI_SIMPLE_SECURITY_HIDE_DOCS`.\n\n## Configuration\n\nEnvironment variables:\n\n- `FASTAPI_SIMPLE_SECURITY_SECRET`: Secret administrator key\n\n    - Generated automatically on server startup if not provided\n    - Allows generation of new API keys, revoking of existing ones, and API key usage view\n    - It being compromised compromises the security of the API\n\n- `FASTAPI_SIMPLE_SECURITY_HIDE_DOCS`: Whether or not to hide the API key related endpoints from the documentation\n- `FASTAPI_SIMPLE_SECURITY_DB_LOCATION`: Location of the local sqlite database file\n    - `sqlite.db` in the running directory by default\n    - When running the app inside Docker, use a bind mount for persistence\n- `FAST_API_SIMPLE_SECURITY_AUTOMATIC_EXPIRATION`: Duration, in days, until an API key is deemed expired\n    - 15 days by default\n\n## Contributing\n\n### Setting up python environment\n\n```shell script\npoetry install\npoetry shell\n```\n\n### Setting up pre-commit hooks\n\n```shell script\npre-commit install\n```\n\n### Running tests\n\n```shell script\npytest\n```\n\n### Running the dev environment\n\nThe attached docker image runs a test app on `localhost:8080` with secret key `TEST_SECRET`. Run it with:\n\n```shell script\ndocker-compose build && docker-compose up\n```\n\n## Needed contributions\n\n- More options with sensible defaults\n- Logging per API key?\n- More back-end options for API key storage?\n',
    'author': 'mrtolkien',
    'author_email': 'gary.mialaret@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mrtolkien/fastapi_simple_security',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4',
}


setup(**setup_kwargs)
