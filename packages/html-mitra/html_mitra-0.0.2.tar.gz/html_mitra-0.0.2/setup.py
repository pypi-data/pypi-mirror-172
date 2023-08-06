from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'html-mitra is a underdevelopment package for editing, creating and serving html files using python'
LONG_DESCRIPTION = 'A package to edit,create and serve HTML files'

# Setting up
setup(
    name="html_mitra",
    version=VERSION,
    author="Developer Gautam Kumar",
    author_email="useronelaptop001@gmail.com",
    description="Create , edit html files easily with preformatted headers and preview them on your localhost or as a file.",
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'html', 'html_mitra', 'dev_gautam', 'nepal'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)