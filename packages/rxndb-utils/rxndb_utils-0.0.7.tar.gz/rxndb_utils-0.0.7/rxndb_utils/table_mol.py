#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/9 21:23
# @Author  : zbc@mail.ustc.edu.cn
# @File    : table_mol.py
# @Software: PyCharm


from rxndb_utils.db_base import DBBase


class TableMol(DBBase):

    def __init__(self, host: str, port: int, database: str, user: str, password: str,
                 table_name: str = 'base.mol'):
        super(TableMol, self).__init__(host, port, database, user, password)
        self._cols = ['mid', 'smiles', 'inchi', 'mol_block']
        self._table_name = table_name

    def set_mol_value(self, column: str, value: str, mid: int, commit: bool = True):
        sql = f"update {self._table_name} set {column}='{value}' where mid={mid}"
        self.exec(sql, commit=commit)

    def get_mol_max_mid(self):
        sql = f"select max(mid) from {self._table_name}"
        return self.select(sql)[0]

    def get_mol_with_smiles(self, smiles: str):
        mols = list(self.get_data_iter(self._table_name, self._cols, f"WHERE smiles='{smiles}'"))
        if len(mols) == 0:
            return None
        else:
            return mols[0]

    def get_all_mols(self):
        for mol in self.get_data_iter(self._table_name, self._cols, None):
            yield mol

    def get_max_mid(self):
        sql = f"select MAX(mid) from {self._table_name}"
        self._cur.execute(sql)
        max_mid = self._cur.fetchone()[0]
        return max_mid

    def add_mol(self, smiles, inchi, mid: int = None, commit: bool = True):
        if mid is None:
            max_mid = self.get_max_mid()
            mid = max_mid + 1
            # sql = f"insert into {self._table_name} (smiles, inchi) values ('{smiles}', '{inchi}')"
        # else:
        sql = f"insert into {self._table_name} (mid, smiles, inchi) values ({mid}, '{smiles}', '{inchi}')"
        # print(sql)
        self.exec(sql, commit)

    def add_or_query_mol_with_smiles(self, smiles: str, inchi: str):
        mol = self.get_mol_with_smiles(smiles)
        if mol is not None:
            return mol['mid']
        else:
            self.add_mol(smiles, inchi, mid=None, commit=True)
            mol = self.get_mol_with_smiles(smiles)
            return mol['mid']

    def get_mol_block_by_smiles(self, smiles: str):
        mol = self.get_mol_with_smiles(smiles)
        if mol is None:
            return None
        else:
            return mol['mol_block']

    def commit(self):
        self.commit()


if __name__ == "__main__":
    smi = "CC(NC(=O)NC1CCN(C1)C1CCCC1)c1cn(nc1C)C(C)(C)C"
    # dbb = DBBase("114.214.205.122", 1684, "rxndb", "postgres", "65zm]+7[d1Kb")
    tm = TableMol("114.214.205.122", 1684, "rxndb", "postgres", "65zm]+7[d1Kb")
    print(tm.get_mol_block_by_smiles('CCc1nnc(CNC(=O)NC2CCN(C)CC2)s1'))
    # print(tm.get_mol_max_mid())
    # print(tm.get_mol_with_smiles(smi))
