#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 14:56
# @Author  : zbc@mail.ustc.edu.cn
# @File    : setup.py
# @Software: PyCharm

from setuptools import setup

with open('README.md', 'r', encoding='utf-8')as f:
    long_description = f.read()

setup(
    name='rxndb_utils',
    version='0.0.7',
    author='zbc',
    author_email='zbc@mail.ustc.edu.cn',
    url='https://github.com/zbc0315/rxndb_utils',
    description=u'reaction database utils',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['rxndb_utils'],
    install_requires=['psycopg2', 'chem-utils', 'rdkit'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)


if __name__ == "__main__":
    pass
