# Author: HIGASHIKAWAUCHI Naofumi <system@interman.jp>
# Copyright (c) 2022- Interman Co., Ltd
# Licence: Apache Software License

from setuptools import setup

DESCRIPTION = 'kanji2arabic: Convert a string of Japanese numerals to Arabic numerals.'
NAME = 'kanji2arabic'
AUTHOR = 'Naofumi Higashikawauchi'
AUTHOR_EMAIL = 'system@interman.co.jp'
URL = 'https://github.com/interman-corp/kanji2arabic.git'
LICENSE = 'License :: OSI Approved :: Apache Software License'
DOWNLOAD_URL = URL
VERSION = '1.0.1'
PYTHON_REQUIRES = '>=3.6'
INSTALL_REQUIRES = [
    'kanjize>=1.0'
]
PACKAGES = [
    'kanji2arabic'
]
KEYWORDS = 'kanji arabic'
CLASSIFIERS=[
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3.6'
]
with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()
LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    download_url=URL,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    install_requires=INSTALL_REQUIRES
)