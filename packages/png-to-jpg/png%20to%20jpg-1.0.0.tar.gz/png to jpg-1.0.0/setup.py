from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'png to jpg'
LONG_DESCRIPTION = 'A package that allows to convert png to jpg'

# Setting up
setup(
    name="png to jpg",
    version=VERSION,
    author="Farooq",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pillow'],
    keywords=['python', 'jpg png','jpg']
)
