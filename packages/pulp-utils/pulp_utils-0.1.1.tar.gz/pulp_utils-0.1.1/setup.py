from setuptools import setup, find_packages
import pulp_utils

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="pulp_utils",
    version=pulp_utils.__version__,
    author="Wira Dharma Kencana Putra",
    author_email="wiradharma_kencanaputra@yahoo.com",
    description="pulp_utils is a library with utility tools for PuLP",
    long_description=description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    install_requires=['pulp'],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Natural Language :: Indonesian",
        "Natural Language :: English"
    ],
    keywords="linear programming operations research optimization jcop indonesia",
    url="https://github.com/WiraDKP/pulp_utils"
    
)