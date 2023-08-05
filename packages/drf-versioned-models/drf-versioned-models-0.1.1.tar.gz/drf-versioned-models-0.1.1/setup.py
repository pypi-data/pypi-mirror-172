from setuptools import setup
import os

VERSION = "0.1.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="drf-versioned-models",
    description="drf-versioned-models is now drf-versioned-schemas",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=["drf-versioned-schemas"],
    classifiers=["Development Status :: 7 - Inactive"],
)
