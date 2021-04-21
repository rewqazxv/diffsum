#!/usr/bin/env python3

import sys
from collections import defaultdict

from typing import Iterable
from typing import Tuple
from typing import Dict
from typing import List


def read_checksum_file(filepath) -> Dict[str, str]:
    """
    read output of checksum programs
    :param filepath: checksum file path
    :return: path-hash map(dict)
    """
    res = dict()
    with open(filepath, encoding='utf-8') as f:
        for i in f:
            checksum, path = i.rstrip('\n').split(' ', 1)
            path = path.lstrip('*')
            res[path] = checksum
    return res


def hash_index(items: Iterable[Tuple[str, str]]) -> Dict[str, List[str]]:
    """
    make hash index
    :param items: collection of path-hash pairs
    :return: hash-paths dict
    """
    res = defaultdict(list)
    for path, checksum in items:
        res[checksum].append(path)
    for i in res:
        res[i].sort(reverse=True)
    return res


if __name__ == '__main__':
    checksums_old = read_checksum_file(sys.argv[1])
    checksums_new = read_checksum_file(sys.argv[2])

    # remove, add, common, change
    paths_old = checksums_old.keys()
    paths_new = checksums_new.keys()
    remove = paths_old - paths_new
    add = paths_new - paths_old
    common = {i[0] for i in checksums_old.items() & checksums_new.items()}
    change = paths_old & paths_new - common

    # select move from remove and add
    move = dict()
    hash_remove = hash_index((k, checksums_old[k]) for k in remove)
    hash_add = hash_index((k, checksums_new[k]) for k in add)
    same_hashs = hash_remove.keys() & hash_add.keys()
    for i in same_hashs:
        paths_remove = hash_remove[i]
        paths_add = hash_add[i]
        while paths_remove and paths_add:
            move[paths_remove.pop()] = paths_add.pop()
    remove -= move.keys()
    add = add.difference(move.values())


    def print_paths(title, paths):
        tab = 2
        leading = ' ' * tab
        if paths:
            print(title + ':')
            if isinstance(paths, set):
                for i in sorted(paths):
                    print(leading, i, sep='')
            elif isinstance(paths, dict):
                for k in paths:
                    v = paths[k]
                    print(leading, k + ' -> ' + v, sep='')


    print_paths('change', change)
    print_paths('remove', remove)
    print_paths('move', move)
    print_paths('add', add)
    # print_paths('common', common)
