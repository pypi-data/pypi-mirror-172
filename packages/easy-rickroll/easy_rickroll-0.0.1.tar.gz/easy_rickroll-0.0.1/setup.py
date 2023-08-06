from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'

# Setting up
setup(
    name="easy_rickroll",
    version=VERSION,
    author="LapisPheonixYT",
    author_email="lapispheonixyt@gmail.com",
    packages=find_packages(),
    install_requires=[],
    keywords=['troll', 'joke', 'meme'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)