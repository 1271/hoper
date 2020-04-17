#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function

from setuptools import setup, find_packages
from hoper.meta import *

REQUIREMENTS = [
    'requests',
    'urllib3',
]


long_description = """
Url redirects history assistant

Please see https://github.com/1271/hoper
"""

release_status = 'Development Status :: 5 - Production/Stable'
if ~version.find('beta'):
    release_status = 'Development Status :: 4 - Beta'
if ~version.find('alpha'):
    release_status = 'Development Status :: 3 - Alpha'


setup(
    name='hoper',
    packages=find_packages(exclude=('.mypy_cache', 'venv', 'tests')),
    include_package_data=True,
    version=version,
    description='Url redirects history assistant',
    long_description=long_description,
    author=author,
    author_email=email,
    url=downloader_url,
    zip_safe=False,
    download_url='{}/archive/{}.tar.gz'.format(downloader_url, version),
    keywords=['hoper', 'redirects', 'url analyze'],
    license='MIT',
    classifiers=[  # look here https://pypi.python.org/pypi?%3Aaction=list_classifiers
        release_status,
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Environment :: Console',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.6',
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'hoper = hoper.hoper:main',
        ]
    }
)
