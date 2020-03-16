# -*- coding: utf-8 -*-
"""
@create: 2020-03-15 11:38:14.

@author: ppolxda

@desc: java_maker
"""
from setuptools import setup, find_packages


setup(
    name="java_maker",
    version="0.0.1",
    install_requires=[
        'six',
        'mako',
    ],
    packages=find_packages('.'),
    package_data={
        '': ['*.txt', '*.md', '*.tmpl', '*.tmlp',
             '*.jinja', '*.json', '*.csv', '*.ts', '*.sql'],
    },
    entry_points={
        "console_scripts": [
            "pydbgen=java_maker.query.main:main",
        ]
    },
    python_requires=">=3.7",
    author="",
    author_email="",
    description="",
    license="",
    keywords="",
    # url="http://example.com/HelloWorld/",
)
