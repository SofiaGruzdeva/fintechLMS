#!/usr/bin/env python3

"""Setup script."""

from setuptools import setup

setup(
    name="lms",
    version="0.0.0",
    author="Gruzdeva Sofia",
    author_email="gruzdeva@phystech.edu",
    url="https://github.com/SofiaGruzdeva/fintechHangman",
    license="MIT",
    packages=[
        "lms",
    ],
    install_requires=[
    ],
    setup_requires=[
        "pytest-runner",
        "pytest-pylint",
        "pytest-pycodestyle",
        "pytest-pep257",
        "pytest-cov",
        "flask",
        "Flask-SQLAlchemy",
        "flask_script",
        "flask_migrate",
        "marshmallow",
        "jwt"
    ],
    tests_require=[
        "pytest",
        "pylint",
        "pycodestyle",
        "pep257",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ]
)
