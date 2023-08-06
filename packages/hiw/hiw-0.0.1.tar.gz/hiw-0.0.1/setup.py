from ast import keyword
from setuptools import setup, find_packages 
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

DESCRIPTION = 'python for abc'

setup(
    name = "hiw",
    version = "0.0.1",
    author = "Duc_Ngoc",
    author_email = "nguyenducngoc167@gmail.com",
    description = DESCRIPTION,
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages=find_packages(),
    keyword=['hiw'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
   
)