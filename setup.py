try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

config = {
  'description': '',
  'author': '',
  'url': '',
  'download_url': '',
  'author_email': '',
  'version': '0.1',
  'install_requires': ['nose'],
  'packages': ['ipfilter_updater'],
  'scripts': [],
  'name': ''
}

setup(**config)
