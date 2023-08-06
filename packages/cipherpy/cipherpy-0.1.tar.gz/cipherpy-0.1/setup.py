from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1'
DESCRIPTION = 'A ciphering library'
LONG_DESCRIPTION = 'A library that can be used to cipher and decipher text using various methods.'

# Setting up
setup(
    name="cipherpy",
    version=VERSION,
    author="Soumil30 (Soumil Gupta)",
    author_email="<soumil009@outlook.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'cipher', 'decipher', 'ciphering', 'deciphering', 'cipherpy', 'encryption', 'decryption',
              'text distortion', 'text', 'text manipulation', 'text processing', 'text ciphering', 'text deciphering'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)