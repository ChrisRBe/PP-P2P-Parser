"""
setup.py for creating packages
"""
from setuptools import setup

setup(
    name="PP-P2P-Parser",
    version="1.0",
    packages=["src", "src.test"],
    url="https://github.com/ChrisRBe/PP-P2P-Parser",
    license="GPL-3.0",
    author="ChrisRBe",
    author_email="chrisrbe@outlook.com",
    description="Parser for P2P services like mintos.com for Portfolio Performance.",
)
