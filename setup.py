#!/usr/bin/env python

from setuptools import setup


readme = open("README.md").read()


setup(
    name="airbrake-tornado",
    version="0.0.1",
    description="Airbrake notifier for Tornado web framework.",
    long_description=readme,
    author="Karlis Lauva",
    author_email="skazhy@gmail.com",
    url="https://github.com/fullcontact/airbrake-tornado",
    license="MIT",
    packages=["airbrake"],
    install_requires=[
        "tornado>=3.2",
    ],
)
