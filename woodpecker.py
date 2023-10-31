"""Script to recursively extract archives and compressed files."""

import argparse
import os
import re
import subprocess
import logging
import magic

from pathlib import Path

def cli() -> dict[str, str]:
    """Return parsed cli."""
    parser = argparse.ArgumentParser(prog="woodpecker",
        description="Recursively extract archives and compressed files.")
    parser.add_argument("directory", type=str, default="./"
        , nargs="?", help="directory path to process")
    return vars(parser.parse_args())

def find_files(directory: str) -> list[str]:
    """Find all the files in a given directory."""
    files = []
    for dirpath, _, file_group in os.walk(directory):
        for file in file_group:
            abs_file = Path(dirpath) / file
            files.append(abs_file.resolve())
    return files

def extract(files: list[str]) -> None:
    """Extract files from a given list of archive/compressed files."""
    for file in files:
        logging.info(f"Extracting {file}")
        try:
            subprocess.run(["7zz", "x", file, "-o"+file+"_dump"
                            , "-y", "-p1234", "-bse0", "-bso0"], check=True)
            Path(file).unlink()
        except subprocess.CalledProcessError as error:
            logging.info(f"file: \'{file}\'\
                Error type: {type(error)}\nError message: {error}\n")

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
        files = list(filter(lambda file:
            pat.search(magic.from_file(file)), files))
