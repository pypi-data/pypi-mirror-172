from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'Download Video Yotube'
LONG_DESCRIPTION = 'A package that allows to download Youtube video.'

# Setting up
setup(
    name="youtube-video",
    version=VERSION,
    author="Farooq",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pytube'],
    keywords=['python', 'download','youtube']
)
