from setuptools import setup, find_packages  # noqa: H301

NAME = "smscx_client"
VERSION = "0.1.12"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
  "urllib3 >= 1.25.3",
  "python-dateutil",
]

setup(
    name=NAME,
    version=VERSION,
    description="SMS API",
    author="SMS Connexion",
    author_email="dev@sms.cx",
    url="",
    project_urls = {
      'Homepage': 'https://sms.cx',
      'Github': 'https://github.com/smscx/smscx-api-python-library'
    },
    keywords=["SMS", "SMS API", "BULK SMS", "VALIDATE PHONE NUMBERS", "RENT PHONE NUMBERS"],
    python_requires=">=3.6",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="Apache-2.0",
)
