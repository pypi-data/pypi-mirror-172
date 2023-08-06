#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/22 16:32
# @Author  : zhangbc0315@outlook.com
# @File    : table_rxn.py
# @Software: PyCharm

from rdkit.Chem import AllChem

from rxndb_utils.db_base import DBBase
from rxndb_utils.table_mol import TableMol
from rxndb_utils.sql_utils import SQLUtils


class TableRxn(DBBase):

    def __init__(self, host: str, port: int, database: str, user: str, password: str,
                 table_name: str = 'base.rxn'):
        super(TableRxn, self).__init__(host, port, database, user, password)
        self._cols = ['rid', 'rxn_code', 'reactants_ids', 'products_ids', 'catalysts_ids', 'solvents_ids',
                      'rxn_smiles', 'product_yield', 'time_year']
        self._table_name = table_name

    def get_rxn_with_rxn_code(self, rxn_code: str):
        rxns = list(self.get_data_iter(self._table_name, self._cols, f"WHERE rxn_code='{rxn_code}'"))
        if len(rxns) == 0:
            return None
        else:
            return rxns[0]

    def get_rxns_with_p_mid(self, p_mid: int):
        rxns = list(self.get_data_iter(self._table_name, self._cols, f"WHERE {p_mid} IN products_ids"))
        return rxns

    def get_rxn_with_rid(self, rid: int):
        rxns = list(self.get_data_iter(self._table_name, self._cols, f"WHERE rid={rid}"))
        if len(rxns) == 0:
            return None
        else:
            return rxns[0]

    def get_all_rxn(self):
        for rxn in self.get_data_iter(self._table_name, self._cols, "ORDER by rid"):
            yield rxn

    def add_rxn(self, rid, rxn_code, reactants_ids, products_ids, catalysts_ids, solvents_ids, rxn_smiles):
        rs_sql = SQLUtils.num_array_to_sql(reactants_ids)
        ps_sql = SQLUtils.num_array_to_sql(products_ids)
        cats_sql = SQLUtils.num_array_to_sql(catalysts_ids)
        sols_sql = SQLUtils.num_array_to_sql(solvents_ids)
        sql = f"insert into {self._table_name} " \
              f"(rid, rxn_code, reactants_ids, products_ids, catalysts_ids, solvents_ids, rxn_smiles) values " \
              f"({rid}, '{rxn_code}', '{rs_sql}', '{ps_sql}', '{cats_sql}', '{sols_sql}', '{rxn_smiles}')"
        self.exec(sql, commit=True)

    def add_rxn_by_rdrxn(self, rid: int, rdrxn: AllChem.ChemicalReaction, table_mol: TableMol,
                         catalysts_smis: [str], solvents_smis: [str], check_dup: bool):
        rxn_code, rs_mids, ps_mids = self._rxn_to_code(rdrxn, table_mol)
        if check_dup:
            rxn = self.get_rxn_with_rxn_code(rxn_code)
        else:
            rxn = self.get_rxn_with_rid(rid)
        if rxn is None:
            rxn_smiles = AllChem.ReactionToSmiles(rdrxn)
            cats_mids = self._get_mids_by_smis(catalysts_smis, table_mol)
            sols_mids = self._get_mids_by_smis(solvents_smis, table_mol)
            cats_sql = SQLUtils.num_array_to_sql(cats_mids)
            sols_sql = SQLUtils.num_array_to_sql(sols_mids)
            rs_sql = SQLUtils.num_array_to_sql(rs_mids)
            ps_sql = SQLUtils.num_array_to_sql(ps_mids)
            sql = f"insert into {self._table_name} " \
                  f"(rid, rxn_code, reactants_ids, products_ids, catalysts_ids, solvents_ids, " \
                  f"rxn_smiles) values " \
                  f"({rid}, '{rxn_code}', '{rs_sql}', '{ps_sql}', '{cats_sql}', '{sols_sql}', " \
                  f"'{rxn_smiles}')"
            self.exec(sql, commit=True)
            return 1
        return 0

    # region ===== rxn utils =====

    @classmethod
    def _get_mids_by_smis(cls, smis: [str], table_mol: TableMol) -> [int]:
        mids = []
        for smi in smis:
            mol = AllChem.MolFromSmiles(smi)
            if mol is None:
                continue
            inchi = AllChem.MolToInchi(mol)
            mids.append(table_mol.add_or_query_mol_with_smiles(smi, inchi))
        return mids

    @classmethod
    def _rxn_to_code(cls, rdrxn: AllChem.ChemicalReaction, table_mol: TableMol) -> str:
        r_mids = []
        p_mids = []
        for reactant in rdrxn.GetReactants():
            smiles = AllChem.MolToSmiles(reactant)
            inchi = AllChem.MolToInchi(reactant)
            mid = table_mol.add_or_query_mol_with_smiles(smiles, inchi)
            r_mids.append(mid)
        for product in rdrxn.GetProducts():
            smiles = AllChem.MolToSmiles(product)
            inchi = AllChem.MolToInchi(product)
            mid = table_mol.add_or_query_mol_with_smiles(smiles, inchi)
            p_mids.append(mid)
        rs_code = '.'.join([str(mid) for mid in sorted(r_mids)])
        ps_code = '.'.join([str(mid) for mid in sorted(p_mids)])
        return f"{rs_code}>>{ps_code}", r_mids, p_mids

    # endregion


if __name__ == "__main__":
    pass
