"""
A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='jsonstrip',
    version='22.10.20',
    description='A Python module for stripping comments from JSON',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/xitop/jsonstrip',

    # Author details
    author='Vlado Potisk',
    author_email='jsonstrip@poti.sk',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Filters',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],

    python_requires='>=3.7',
    scripts=['jsoncheck'],
    py_modules=["jsonstrip"],

    project_urls={
        "Source": "https://github.com/xitop/jsonstrip/",
    },
)
