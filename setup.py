import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

requires = [
    'barbecue',
    'boto',
    'chaussette',
    'cornice',
    'couchdb-schematics',
    'gevent',
    'iso8601',
    'jsonpatch',
    'pbkdf2',
    'pycrypto',
    'pyramid_exclog',
    'rfc6266',
    'setuptools',
    'tzlocal',
    'openprocurement.api'
]

test_requires = requires + [
    'openprocurement.api',
    'webtest',
]

entry_points = """\
[paste.app_factory]
main = openprocurement.planning:main
"""

setup(name='openprocurement.planning',
      version='0.2',
      description='Planning API to openprocurement',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      keywords="web services",
      author='Quintagroup, Ltd.',
      author_email='info@quintagroup.com',
      license='Apache License 2.0',
      url='https://github.com/gorserg/openprocurement.planning',
      package_dir = {'': 'src'},
      packages=find_packages('src'),
      namespace_packages = ['openprocurement', 'openprocurement.planning'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=test_requires,
      extras_require={'test': test_requires},
      test_suite="openprocurement.planning.api.tests.main.suite",
      entry_points = entry_points)
