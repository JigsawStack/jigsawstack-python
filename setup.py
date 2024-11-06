#!/usr/bin/env python

from setuptools import find_packages, setup

install_requires = open("requirements.txt").readlines()

setup(
    name="jigsawstack",
    version="0.1.18",
    description="JigsawStack Python SDK",
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    author="Narcisse Egonu",
    author_email="hello@jigsawstack.com",
    url="https://github.com/jigsawstack/jigsawstack-python",
    packages=find_packages(include=["jigsawstack"]),
    install_requires=install_requires,
    zip_safe=False,
    python_requires=">=3.7",
    keywords=["AI", "AI Tooling"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
