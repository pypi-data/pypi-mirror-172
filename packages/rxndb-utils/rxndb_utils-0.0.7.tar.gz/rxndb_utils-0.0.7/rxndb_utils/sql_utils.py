#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/8/22 14:34
# @Author  : zhangbc0315@outlook.com
# @File    : sql_utils.py
# @Software: PyCharm


class SQLUtils:

    @classmethod
    def num_array_to_sql(cls, array: [int]) -> str:
        _array = [str(d) for d in array]
        return '{' + ','.join(_array) + '}'


if __name__ == "__main__":
    pass
