import os
from setuptools import setup, find_packages

from lightweight_environ import __version__

# allow setup.py to be run from any path

with open('README.md') as readme_md:
    README = readme_md.read()

setup(
    name='lightweight-environ',
    version=__version__,
    author='Patrick Smith',
    license='MIT',
    description='Simple and lightweight environment variable ingestion',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/cursive-works/lightweight-environ',
    keywords=['environment variables','configuration'],

    py_modules = ['lightweight_environ'],
    install_requires=[],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
    ],
)
