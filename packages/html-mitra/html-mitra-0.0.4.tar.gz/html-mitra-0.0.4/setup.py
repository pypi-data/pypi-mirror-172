from setuptools import setup, find_packages
import codecs
import os
from pathlib import Path
VERSION = '0.0.4'
DESCRIPTION = 'html-mitra is a underdevelopment package for editing, creating and serving html files using python'

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="html-mitra",
    version=VERSION,
    author="Developer Gautam Kumar",
    author_email="useronelaptop001@gmail.com",
    description="Create , edit html files easily with preformatted headers and preview them on your localhost or as a file.",
    long_description_content_type="text/markdown",
    long_description=long_description,
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