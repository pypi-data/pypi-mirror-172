#!/usr/bin/env python

from distutils.core import setup

setup(
    name="pycfs",
    version="0.0.1",
    description="OpenCFS automatization and optimization interface library for python.",
    author="Eniz Museljic",
    author_email="eniz.m@outlook.com",
    url="https://www.tugraz.at/institute/igte/home/",
    packages=["pycfs", "pycfs.optimization", "pycfs.util"],
    include_package_data=True,
    keywords=["optimization", "opencfs", "simulation", "finite elements"],
    install_requires=["numpy>=1.20.1",
                      "typing_extensions>=3.7.4.3",
                      "glob2>=0.7",
                      "pytest>=6.2.5",
                      "h5py",
                      "matplotlib",
                      "tqdm",
                      ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
)
