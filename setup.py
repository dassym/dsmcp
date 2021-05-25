from setuptools import setup, setuptools
import sys, os
sys.path.insert(0, os.path.abspath('./src/dsmcp/app'))
from _version import __version__ as APP_VERSION
from common import APP_NAME

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
  
setup(
    name=APP_NAME,
    version=APP_VERSION,
    author="Fabrice Voillat",
    author_email="dev@dassym.com",
    description="The PyDapi2 library offers a Python implementation of the Dassym API version 2.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = ['lxml', 'pyserial', 'PyDapi2', 'chardet'],
    url="https://github.com/dassym/dsmcp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    include_package_data=True
)