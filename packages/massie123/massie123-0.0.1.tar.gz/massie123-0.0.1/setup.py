from setuptools import setup, find_packages
import codecs
import os

VERSION = "0.0.1"
DESCRIPTION = "A basic hello package"
LONG_DESCRIPTION = "A basic hello package long description!"

# Setting up
setup(
    name="massie123",
    version=VERSION,
    author="Massie Mahmoodi",
    author_email="<mail@anu.edu.au>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["python"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
