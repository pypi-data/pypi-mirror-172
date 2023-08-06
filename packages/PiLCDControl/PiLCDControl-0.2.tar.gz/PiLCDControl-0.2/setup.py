# Copyright (c) 2022, Adam Lake
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# ======================================================================================================================
# Created: 18/10/2022
# GitHub: https://github.com/adam1lake/Pi-LCD
# ======================================================================================================================

from setuptools import setup, find_packages

NAME = "PiLCDControl"
VERSION = "0.2"
DESCRIPTION = "A simple interface to common 16x2 Raspberry Pi LCD screens (HD44780)."
LONG_DESCRIPTION = "A simple interface to common 16x2 Raspberry Pi LCD screens (HD44780). Includes useful features " \
                   "such as:" \
                   "\n- Text display" \
                   "\n- Timeouts and delays" \
                   "\n- Text scrolling" \
                   "\n- Threading to allow for control of both lines separately" \
                   "\n- Logic to prevent display \"glitches\" when performing multiple operations at once"
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Operating System :: POSIX :: Linux",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Home Automation",
    "Topic :: Software Development",
    "Topic :: System :: Hardware"
]

setup(
    name=NAME,
    version=VERSION,
    author="Adam Lake",
    author_email="adam1lake@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["RPi.GPIO"],
    keywords=["python", "raspberry pi", "lcd"],
    license="BS2",
    url="",
    classifiers=CLASSIFIERS
)
