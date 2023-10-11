import os
import re
import magic
import argparse
import subprocess

def cli():
	parser = argparse.ArgumentParser(prog='woodpecker',
        description='Recursively extract archives and compressed files.')
	parser.add_argument("directory", type=str, default='./'
                , nargs='?', help="directory path to process")
	return parser.parse_args()

def find_files(directory):
    files = []
    for dirpath, _, file_group in os.walk(directory):
        for file in file_group:
            file = os.path.abspath(os.path.join(dirpath, file))
            files.append(file)
    return files

def extract(files):
    for file in files:
        print(f'Extracting {file}')
        try:
            subprocess.run(['7zz', 'x', file, '-o'+file+'_dump'
                            , '-y', '-p1234', '-bse0', '-bso0'], check=True)
            os.remove(file)
        except Exception as e:
            print(f'file: \'{file}\'\nError type: {type(e)}\nError message: {e}\n')

if __name__ == "__main__":

    pat = re.compile(r'archive|compress', re.IGNORECASE)

    # Parsing CLI
    args = cli()

    # Extracting files
    files = find_files(directory=args.directory)
    files = list(filter(lambda file: pat.search(magic.from_file(file)), files))
    errors = []
    all_files = set()

    while len(files) > 0:
        files = [file for file in files if file not in all_files]
        all_files.update(set(files))

        if len(files) == 0:
            break
        extract(files)

        files = find_files(directory=args.directory)
        files = list(filter(lambda file: pat.search(magic.from_file(file)), files))
