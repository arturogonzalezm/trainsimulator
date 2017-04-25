from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from os import path
import io

from trainsimulator.version import __version__, __url__, __license__, __author__, __email__

here = path.abspath(path.dirname(__file__))

try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    print("Can't import pypandoc - using README.md without converting to RST")
    long_description = open('README.md').read()

NAME = 'trainsimulator'
with io.open(path.join(here, NAME, 'version.py'), 'rt', encoding='UTF-8') as f:
    exec(f.read())

setup(
    name=NAME,
    version=__version__,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*', 'examples*']),
    url=__url__,
    license=__license__,
    author=__author__,
    author_email=__email__,
    long_description=long_description,
    description=''
)
