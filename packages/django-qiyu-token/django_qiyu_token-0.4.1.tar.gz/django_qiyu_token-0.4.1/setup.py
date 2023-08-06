# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_qiyu_token',
 'django_qiyu_token.admin',
 'django_qiyu_token.migrations',
 'django_qiyu_token.models']

package_data = \
{'': ['*'],
 'django_qiyu_token': ['locale/en/LC_MESSAGES/*', 'locale/zh/LC_MESSAGES/*']}

install_requires = \
['django-ninja>=0.19,<0.20', 'django>=3.2,<4.2', 'pyjwt[crypto]>=2.1,<3.0']

setup_kwargs = {
    'name': 'django-qiyu-token',
    'version': '0.4.1',
    'description': 'Django Token Management APP',
    'long_description': '# Django 令牌管理\n\n## 当前支持:\n\n* Bearer 令牌\n* Json Web Token 令牌\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://oss.qiyutech.tech/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
