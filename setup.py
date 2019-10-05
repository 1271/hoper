#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function

from setuptools import setup
from .hoper.meta import version, author

REQUIREMENTS = [
    'requests',
    'urllib3',
]


long_description = 'Please see https://github.com/1271/hoper'

release_status = 'Development Status :: 5 - Production/Stable'


setup(
    name='manga_py',
    packages=[
        'manga_py',
        'manga_py.base_classes',
        'manga_py.crypt',
        'manga_py.cli',
        'manga_py.http',
        'manga_py.providers',
        'manga_py.providers.helpers',
        'manga_py.server',
    ],
    include_package_data=True,
    version=version,
    description='Universal assistant download manga.',
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.5',
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'hoper = hoper:main',
        ]
    }
)
