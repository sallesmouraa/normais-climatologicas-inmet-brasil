from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="normais-climatologicas-inmet",
    version="0.1.0",
    author="Salles Moura",
    author_email="sallesmouraa@github.com",
    description="API para consulta de Normais Climatológicas do Brasil (1991-2020)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sallesmouraa/normais-climatologicas-inmet-brasil",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
    ],
    include_package_data=True,
    keywords=[
        "clima",
        "climatologia",
        "brasil",
        "INMET",
        "normais-climatologicas",
        "geospatial",
        "geoprocessamento",
        "sensoriamento-remoto",
    ],
)
