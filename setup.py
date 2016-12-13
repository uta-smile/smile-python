"""Setup file for SMILE-python package."""

import os
from setuptools import setup

CURRENT_DIR = os.path.dirname(__file__)
__version__ = "0.0.2"

setup(
    name="smile",
    version=__version__,
    description=open(os.path.join(CURRENT_DIR, "README.md")).read(),
    install_requires=[],
    author="Zheng Xu",
    author_email="zheng.xu@mavs.uta.edu",
    zip_safe=False,
    packages=["smile"],
    package_data={".": ["README.md"]},
    url="https://github.com/uta-smile/smile-python/"
)
