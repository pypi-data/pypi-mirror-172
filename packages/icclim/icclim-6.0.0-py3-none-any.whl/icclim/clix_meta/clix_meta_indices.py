from __future__ import annotations

""" Wrapper for clix-meta yaml file.
    This read the yaml and make its content accessible an instance of ClixMetaIndices.
    It also exposes some type hints of yaml content.
"""
import os
from pathlib import Path
from typing import Any, TypedDict
from functools import reduce

import yaml

CLIX_YAML_PATH = (
    Path(os.path.dirname(os.path.abspath(__file__))) / "index_definitions.yml"
)


class EtMetadata(TypedDict):
    short_name: str
    long_name: str
    definition: str
    comment: str


class OutputMetadata(TypedDict):
    var_name: str
    standard_name: str
    long_name: str
    units: str
    cell_methods: dict


class ClixMetaIndex(TypedDict):
    reference: str
    period: dict
    output: OutputMetadata
    input: dict
    index_function: dict
    ET: EtMetadata


class ClixMetaIndices:
    """Singleton to access content of clix-meta yaml file.
    """

    __instance: Any = None
    indices_record: dict[str, ClixMetaIndex]

    @staticmethod
    def get_instance() -> ClixMetaIndices:
        if ClixMetaIndices.__instance is None:
            ClixMetaIndices.__instance = ClixMetaIndices()
        return ClixMetaIndices.__instance

    def __init__(self):
        if ClixMetaIndices.__instance is not None:
            raise Exception("This class is a singleton! Use Clix::get_instance.")
        else:
            ClixMetaIndices.__instance = self
            with open(CLIX_YAML_PATH, "r") as clix_meta_file:
                self.indices_record = yaml.safe_load(clix_meta_file)["indices"]

    def lookup(self, query: str) -> ClixMetaIndex | None:
        for index in self.indices_record.keys():
            if index.upper() == query.upper():
                return self.indices_record[index]
        return None


def sort_by_key(dico: dict, key: str = "reference"):
    filtered =  {k: v for k, v in dico.items() if  v[key] is not None}
    return {k: v for k, v in
            sorted(filtered.items(), key=lambda x: x[1].get(key, "zzzz") or "zzzz")}


def to_rst_table(dico: dict[str, dict[str, str]], key="reference"):
    dico = sort_by_key(dico, key)
    dico = flatten_level_2(dico)
    dico = filter_relevant_keys(dico, [
        "reference",
        "output.var_name",
        "output.standard_name",
        "output.cell_methods",
        "output.long_name",
        "output.units",
        "output.proposed_standard_name",
        "index_function.name",
        "index_function.parameters.reducer.reducer",
    ])
    key_to_max_length_mapper = {}
    inner_keys = reduce(lambda x,y : set(x) | set(y), map(lambda d: list(d.keys()), dico.values()))
    # get maxes
    for inner_key in inner_keys:
        current_max = 0
        for k, v in dico.items():
            val = v.get(inner_key, "")
            if len(str(val)) > current_max:
                current_max = len(str(val))
        key_to_max_length_mapper.update({inner_key: current_max})
    # print table
    mega_acc = ""
    for k in inner_keys:
        length = key_to_max_length_mapper.get(k)
        end_space = " " * (length - len(k))
        mega_acc += f"{k}{end_space} |"
    mega_acc+= "\n"
    for k, v in dico.items():
        string_acc = ""
        for k2 in inner_keys:
            value = str(v.get(k2, "_") or "_")
            length = key_to_max_length_mapper.get(k2)
            end_space = " " * (length - len(value))
            string_acc += f" {value}{end_space} |"
        mega_acc += "\n| " + string_acc
    print(mega_acc)

def filter_relevant_keys(dico: dict, keys: list[str])-> dict:
    filtered_dico = {}
    for k,v in dico.items():
        res = {}
        for key in keys:
            if key in v.keys():
                res.update({key: v[key] })
        filtered_dico.update({k: res})
    return filtered_dico

def flatten_level_2(dico: dict):
    for k, v in dico.items():
        if isinstance(v, dict):
            dico[k] = flatten(v)
        else:
            dico[k] = v
    return dico


def flatten(dico:dict, separator: str = ".") -> dict:
    flat_dict = {}
    for k, v in dico.items():
        if isinstance(v, dict):
            f = flatten(v)
            for k2, v2 in f.items():
                flat_dict[k + separator + k2] = v2
        else:
            flat_dict[k] = v
    return flat_dict
