"""Python setup.py for FEA_Project package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("FEA_Project", "0.1.0")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="FEA_Project",
    version=read("FEA_Project", "0.1.0"),
    description="An FEA Python Program for Euler Bernoulli Beam Analysis.",
    url="https://github.com/raulds-fmtx/FEA-Project.git",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="raulds-fmtx",
    packages=["FEA_Project"],
    entry_points={
        "console_scripts": ["FEA_Project = FEA_Project.__main__:main"]
    },
)