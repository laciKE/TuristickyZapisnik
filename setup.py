from setuptools import setup

import os

# Put here required packages
packages = ['Django<=1.6',]

if 'REDISCLOUD_URL' in os.environ and 'REDISCLOUD_PORT' in os.environ and 'REDISCLOUD_PASSWORD' in os.environ:
     packages.append('django-redis-cache')
     packages.append('hiredis')

setup(name='The Tourist Diary',
      version='1.0',
      description='OpenShift App for Tourists',
      author='LaciKE',
      author_email='lacike3.14+turistika@gmail.com',
      url='https://pypi.python.org/pypi',
      install_requires=packages,
)

