# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import argparse
import json
import random
import subprocess
import typing as tp
from pathlib import Path
from typing import List
from logging import getLogger

from codegen.model.preprocess import XLM_preprocess

REPO_ROOT = str(Path(__file__).parents[2])

FALSY_STRINGS = {"off", "false", "0"}
TRUTHY_STRINGS = {"on", "true", "1"}

logger = getLogger()


def bool_flag(s):
    """
    Parse boolean arguments from the command line.
    """
    if s.lower() in FALSY_STRINGS:
        return False
    elif s.lower() in TRUTHY_STRINGS:
        return True
    else:
        raise argparse.ArgumentTypeError("Invalid value for a boolean flag!")


def is_valid_file(file):
    if file is None:
        return False
    if isinstance(file, str):
        file = Path(file)
    else:
        assert isinstance(file, Path)
    return file.is_file() and file.stat().st_size > 0


def get_nlines(file_path):
    assert file_path.is_file(), file_path
    process = subprocess.run(
        f"wc -l {file_path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert process.returncode == 0
    return int(process.stdout.decode().split(" ")[0])


def check_same_number_of_lines(file_path1, file_path2):
    nlines1 = get_nlines(file_path1)
    nlines2 = get_nlines(file_path2)
    assert nlines1 == nlines2


def head(file_path, n):
    n = int(n)
    with file_path.open("r", encoding="utf-8") as f:
        h = [next(f) for i in range(n)]
    return h


def get_subset_file(file_paths: List[Path], subset_size_gb: int, output_path: Path):
    """
    Return one file containing a subset of files file_paths.
    The subset is of size subset_size_gb.
    The subset contains an equal portion on all files.
    """
    if output_path.is_file():
        return f"{output_path}"
    for file_path in file_paths:
        size_gb = file_path.stat().st_size / 1024 ** 3
        n_lines = get_nlines(file_path)
        subset_n_lines = int((subset_size_gb / len(file_paths)) * (n_lines / size_gb))
        process = subprocess.run(
            f"head -q -n {subset_n_lines} {file_path} >> {output_path}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            executable="/bin/bash",
        )
        assert process.returncode == 0
    logger.info(
        f"Subset of {[f.name for f in file_paths]} created at: {output_path.name}. Size=({output_path.stat().st_size / 1024 ** 3:.2f}GB)."
    )
    return f"{output_path}"


def truncate_files(file_paths):
    all_lines = []
    for f in file_paths:
        with f.open("r", encoding="utf-8") as f:
            lines = f.readlines()
            all_lines.append(lines)
    mini = min([len(lines) for lines in all_lines])
    for f, i in enumerate(file_paths):
        if len(all_lines[i]) > mini:
            with f.open("w", encoding="utf-8") as f:
                for j in range(mini):
                    f.write(all_lines[i][j])


def write_head(file_path, n):
    n = int(n)
    with file_path.open("r", encoding="utf-8") as f:
        h = [next(f) for i in range(n)]
    with file_path.open("w", encoding="utf-8") as f:
        f.write("".join(h))
    return h


def shuf_file(file_path):
    process = subprocess.run(
        f"shuf {file_path} -o {file_path}.shuf",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert (
            process.returncode == 0
    ), f"failed to shuffle {file_path}\n Error {process.stderr}"


def get_all_pairs(items):
    return [
        (items[i], items[j])
        for i in range(len(items))
        for j in range(i + 1, len(items))
    ]


def shuf_parallel_files(file_paths):
    lines_order = []
    for input_path in file_paths:
        with open(input_path, "r") as f:
            lines = f.readlines()
        if not lines_order:
            lines_order = list(range(len(lines)))
            random.shuffle(lines_order)
            random.shuffle(lines_order)

        assert len(lines_order) == len(
            lines
        ), f"files with different number of lines in {file_paths}"
        reordered = [lines[i] for i in lines_order]
        with open(f"{input_path}.shuf", "w") as f:
            f.writelines(reordered)


def get_repo_to_group_dict(repo_groups_path):
    repo_groups = open(repo_groups_path, "r").read().strip()
    repo_groups_dict = json.loads(repo_groups)
    repo_to_group = dict()
    for k, values in repo_groups_dict.items():
        for v in values:
            assert v not in repo_to_group
            repo_to_group[v] = k
    return repo_to_group


def binarize_for_XLM_file(file_path, vocab):
    assert get_nlines(file_path) > 0
    return XLM_preprocess(str(vocab), str(file_path), str(file_path) + ".pth")


def create_symlink(file_path, symlink):
    if isinstance(file_path, str):
        file_path = Path(file_path)
    if isinstance(symlink, str):
        symlink = Path(symlink)
    assert file_path.is_file(), f"{file_path} is not a file"
    assert not symlink.is_file(), f"{symlink} already exists"
    process = subprocess.run(
        f"ln -s {file_path} {symlink}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert (
            symlink.is_file() and process.returncode == 0
    ), f"failed to create symlink {symlink} for file {file_path} "
