# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drfa']

package_data = \
{'': ['*']}

install_requires = \
['django>=4.1,<5.0', 'djangorestframework>=3.14.0,<4.0.0']

setup_kwargs = {
    'name': 'django-rest-framework-async',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Overview\n\nAdds async support to Django REST Framework.\n\nCurrently not production ready. Use at your own risk :)\n\n# Requirements\n\n- Python 3.10+\n- Django 4.1+\n\n# Installation\n\n```\npip install django-rest-framework-async\n```\n\n# Example\n\n```\nfrom drfa.decorators import api_view\nfrom drfa.views import APIView\n\nclass AsyncView(APIView):\n    async def get(self, request):\n        return Response({"message": "This is an async class based view."})\n\n\n@api_view([\'GET\'])\nasync def async_view(request):\n    return Response({"message": "This is an async function based view."})\n```',
    'author': 'frownyface',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
