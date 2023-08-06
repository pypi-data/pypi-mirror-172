#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/9 21:16
# @Author  : zbc@mail.ustc.edu.cn
# @File    : db_base.py
# @Software: PyCharm

from typing import List, Iterator, Dict, Union
import logging

import psycopg2


class DBBase:

    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        logging.info(f"connecting to database {host}:{port}/{database}")
        self._conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
        self._cur = self._conn.cursor()

    def commit(self):
        self._conn.commit()

    def exec(self, sql: str, commit: bool = True):
        self._cur.execute(sql)
        if commit:
            self._conn.commit()

    def select(self, sql):
        self._cur.execute(sql)
        return self._cur.fetchone()

    def get_data_iter(self, table_name: str, cols: List[str], condition: Union[str, None]) -> Iterator[Dict]:
        self._cur.execute(self._select_sql(table_name, cols, condition))
        while True:
            try:
                res = self._cur.fetchone()
                res_dict = {}
                for col, value in zip(cols, res):
                    res_dict[col] = value
                yield res_dict
            except:
                break

    @staticmethod
    def _select_sql(table_name: str, cols: List[str], condition: str) -> str:
        if condition is not None:
            return f"SELECT {','.join(cols)} " \
                   f"FROM {table_name} " \
                   f"{condition}"
        else:
            return f"SELECT {','.join(cols)} " \
                   f"FROM {table_name} "


if __name__ == "__main__":
    pass
