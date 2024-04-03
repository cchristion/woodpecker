#!/usr/bin/env python3

"""Recursive Compressed and Archived files Extractor."""

import argparse
import logging
import re
import subprocess
import sys
from collections import deque
from pathlib import Path

import magic


def cli() -> dict:
    """CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Recursive Compressed and Archived files Extractor",
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Path to directory",
    )
    parser.add_argument(
        "-e",
        "--extract_using",
        type=str,
        help="Alternative to 7zz to Extract files default: 7zz",
        default=Path("7zz"),
    )
    args = parser.parse_args()
    return vars(args)


def find_files(directory: Path) -> None:
    """Queue all the files in a directory recursively."""
    pat = re.compile(r"archive|compress", re.IGNORECASE)
    for dirpath, _, filenames in directory.walk():
        for file in filenames:
            file_path = Path(dirpath / file).absolute()
            try:
                file_type = magic.from_file(file_path)
            except Exception:
                logging.exception("Unable to determine file type %s", file_type)
                continue
            if pat.search(file_type):
                fileq.append(file_path)
    logging.info("%d files in queue", len(fileq))


def extract(file: Path, app: Path) -> None:
    """Extract archived or compressed file using 7zz."""
    output_dir = str(file) + "_dump"
    cmd = [
        app,
        "x",
        str(file),
        "-o" + output_dir,
        "-y",
        "-p1234",
        "-bse0",
        "-bso0",
    ]
    try:
        logging.info("Extracting: %s", file.name)
        subprocess.run(
            cmd,
            check=True,
        )
        file.unlink()
        logging.info("Extracted: %s", file.name)
        find_files(Path(output_dir))
    except BaseException:
        logging.exception("%s:", file)


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)s : %(levelname)s : %(message)s",
        datefmt="%Y%m%dT%H%M%S",
        encoding="utf-8",
        level=logging.DEBUG,
    )

    args = cli()

    path_7zip = subprocess.getoutput(f"command -v {args['extract_using']}")
    path_7zip = Path(path_7zip)

    if path_7zip == Path():
        logging.error("7zz command not found")
        sys.exit()
    else:
        logging.info("7zz path: %s", path_7zip)

    fileq = deque()
    find_files(args["directory"])

    while fileq:
        extract(file=fileq.popleft(), app=path_7zip)

    logging.info("Extracted all Compressed and Archived files")
