import os
# read the contents of your README file
from pathlib import Path

import pkg_resources
from setuptools import find_packages, setup

long_description = Path(__file__).with_name("README.md").read_text()

version = "0.4.20"

setup(
    name="cypher-to-gremlin",
    packages=find_packages(exclude=("test")),
    version=version,
    license="Apache Software License",
    description="tbd",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="c7nw3r",
    url="https://github.com/c7nw3r/cypher-to-gremlin",
    download_url=f"https://github.com/c7nw3r/cypher-to-gremlin/archive/refs/tags/v{version}.tar.gz",
    keywords=[],
    setup_requires=["setuptools_scm"],
    include_package_data=True,
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: FullText Search",
        "Topic :: Scientific/Engineering :: Semantic Search",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    extras_require={
        "annoy": ["annoy==1.17.3", "pysbd==0.3.4", "numpy"],
        "tantivy": [
            "tantivy@git+https://github.com/leftshiftone/tantivy-py.git#egg=tantivy",
            "stop-words==2018.7.23",
            "simplemma==0.9.1",
            "pysbd==0.3.4",
        ],
        "networkx": ["networkx==3.1"],
    },
)
