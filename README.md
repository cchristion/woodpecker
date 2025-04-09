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
usage: woodpecker.py [-h] [-e EXTRACT_USING] directory

Recursive Compressed and Archived files Extractor

positional arguments:
  directory             Path to directory

options:
  -h, --help            show this help message and exit
  -e EXTRACT_USING, --extract_using EXTRACT_USING
                        Alternative to 7zz to Extract files default: 7zz
```

## Examples

Extract all compressed and archived files in the current directory and its subdirectories:

### Using Python

```shell
pip install --upgrade python-magic # dependency
python woodpecker.py /path/to/extract
```

### Using UV

```shell
uv run woodpecker.py /path/to/extract
```
