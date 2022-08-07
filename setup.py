from setuptools import setup, find_packages
from os import environ
import os

version = os.getenv("GITHUB_REF_NAME", '')
repo = os.getenv("GITHUB_REPOSITORY", '')
github = os.getenv("GITHUB_SERVER_URL")
url = f"{github}/{repo}"

setup(
    name="afip-ws",
    version=version,
    author="Gaston Michel",
    author_email="michel.z.gaston@gmail.com",
    description="Python library to easily interact with AFIP Web Services",
    url=url,
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    packages=find_packages("./afip", exclude="tests"),
    install_requires=open("requirements.txt").readlines(),
    keywords=["afip", "ws", "python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
