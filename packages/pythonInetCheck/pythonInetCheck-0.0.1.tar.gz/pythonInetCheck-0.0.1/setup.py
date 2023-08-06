from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'pythonInetCheck'
LONG_DESCRIPTION = 'a process that checks if a device can connect to the web and notifys the user via system moniter'

# Setting up
setup(
    name="pythonInetCheck",
    version=VERSION,
    author="rosejustin601 (Justin Rose)",
    author_email="rosejustin601@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'internet', 'status', 'test'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
