# woodpecker: Python Script for Recursive Extraction of Compressed and Archived Files

This Python script is designed to recursively extract compressed and archived files from a given directory. It supports various compression formats, including ZIP, RAR, 7Z, and TAR.

## Features

* Recursively searches for compressed and archived files in a specified directory and its subdirectories
* Supports multiple compression formats, including ZIP, RAR, 7Z, and TAR
* Extracts files and directories with the same structure as the original archive
* Handles nested archives (i.e., archives within archives)

## Usage

* Clone this repository and navigate into the woodpecker folder.
* Install dependencies.
* Run python `woodpecker.py` to start the extraction process.
* Follow the command-line interface (CLI) instructions.
* Wait for the extraction process to complete. Depending on the number of files and their sizes, this may take several minutes or longer.
* Verify that all expected files have been extracted successfully by checking the output directory.

## Options

The following options are available when running the script:
```
positional arguments:
  directory   Specifies the path to the directory containing the compressed and archived files.

options:
  -h, --help  show this help message and exit
```

## Examples

Extract all compressed and archived files in the current directory and its subdirectories:
```shell
python woodpecker.py /directory/path
```

## Dependencies

Install these packages before running the script if they are not already installed:
```shell
pip install --upgrade python-magic
```
