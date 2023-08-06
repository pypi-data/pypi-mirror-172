#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/9 21:12
# @Author  : zbc@mail.ustc.edu.cn
# @File    : db_init.py
# @Software: PyCharm

import logging

from rxndb_utils.db_base import DBBase


class DBInit:

    @classmethod
    def init(cls, host: str, port: int, database: str, user: str, password: str):
        dbb = DBBase(host, port, database, user, password)
        sql = f"create schema base;"
        logging.info(f"creating schema: base")
        dbb.commit(sql)
        cls.init_table_mol(dbb)
        cls.init_table_mol_name(dbb)
        cls.init_table_rxn(dbb)

    @classmethod
    def init_table_mol(cls, dbb):
        sql = f"create table base.mol " \
              f"(mid serial constraint mol_pk primary key," \
              f"smiles text not null," \
              f"inchi text not null);"
        logging.info(f"creating table: base.mol")
        dbb.commit(sql)

    @classmethod
    def init_table_mol_name(cls, dbb):
        sql = f"create table base.mol_name " \
              f"(mnid serial constraint mol_name_pk primary key," \
              f"mid int not null," \
              f"name text not null);"
        logging.info(f"creating table: base.mol_name")
        dbb.commit(sql)

    @classmethod
    def init_table_rxn(cls, dbb):
        sql = "create table base.rxn " \
              "(rid serial constraint rxn_pk primary key," \
              "rxn_codes text not null," \
              "reactants_codes integer[] default '{}'," \
              "products_codes integer[] default '{}'," \
              "catalysts_codes integer[] default '{}'," \
              "solvents_codes integer[] default '{}'," \
              "num_reactants int," \
              "num_products int," \
              "num_catalysts int," \
              "num_solvents int," \
              "rxn_smiles text not null," \
              "product_yield float," \
              "year int);"
        logging.info(f"creating table: base.rxn")
        dbb.commit(sql)


if __name__ == "__main__":
    pass
