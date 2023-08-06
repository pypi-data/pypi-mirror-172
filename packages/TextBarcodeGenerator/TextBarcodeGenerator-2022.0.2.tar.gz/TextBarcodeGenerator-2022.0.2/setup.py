"""Set up the build"""
from setuptools import setup

setup(
    name="TextBarcodeGenerator",
    version="2022.0.2",
    description="A tool to generate text-based barcodes.",
    long_description_content_type="text/markdown",
    long_description="This is a tool to generate text-based barcodes. You can "
                     "input anything, so long as it can be converted to a "
                     "numerical string.",
    author="J-J-B-J",
    url="https://github.com/J-J-B-J/BarcodeGenerator",
    keywords="barcode generator text numerical",
    python_requires=">=3.9",
    install_requires=[],
    package_dir={'': '.'},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: Free for non-commercial use",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    platforms=["Windows", "MacOS", "Unix"],
    packages=["BarcodeGenerator"],
)
