"""Python Script for Recursive Extraction of Compressed and Archived Files."""

import argparse
import logging
import os
import re
import subprocess
from pathlib import Path

import magic


def cli() -> dict[str, str]:
    """Return parsed cli."""
    parser = argparse.ArgumentParser(
        prog="woodpecker",
        description="Python Script for Recursive Extraction of Compressed and Archived Files.",
    )
    parser.add_argument(
        "directory",
        type=str,
        default="./",
        nargs="?",
        help="Specifies the path to the directory containing the compressed and archived files.",
    )
    return vars(parser.parse_args())


def find_files(directory: str) -> list[str]:
    """Find all the files in a given directory."""
    file_list = []
    for dirpath, _, file_group in os.walk(directory):
        for file in file_group:
            abs_file = Path(dirpath) / file
            file_list.append(abs_file.resolve())
    return file_list


def extract(file_list: list[str]) -> None:
    """Extract files from a given list of archive/compressed files."""
    for file in file_list:
        cmd = [
            "7zz",
            "x",
            file,
            "-o" + file + "_dump",
            "-y",
            "-p123456",
            "-bse0",
            "-bso0",
        ]
        logging.info("Extracting %s", file)
        try:
            subprocess.run(cmd, check=True)
            Path(file).unlink()
        except subprocess.CalledProcessError as error:
            logging.info(
                "file: %s\
                Error type: %s\
                Error message: %s\n",
                file,
                type(error),
                error,
            )


if __name__ == "__main__":
    pat = re.compile(r"archive|compress", re.IGNORECASE)

    # Parsing CLI
    args = cli()

    # Extracting files
    files = find_files(directory=args["directory"])
    files = list(filter(lambda file: pat.search(magic.from_file(file)), files))
    errors = []
    all_files = set()

    while len(files) > 0:
        files = [file for file in files if file not in all_files]
        all_files.update(set(files))

        if len(files) == 0:
            break
        extract(files)

        files = find_files(directory=args["directory"])
        files = list(
            filter(lambda file: pat.search(magic.from_file(file)), files),
        )
