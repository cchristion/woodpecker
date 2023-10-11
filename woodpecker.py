import argparse

def cli():
	parser = argparse.ArgumentParser(prog='woodpecker',
        description='Recursively extract archives and compressed files.')
	parser.add_argument("directory", type=str, default='./' , nargs='?', help="directory path to process")
	return parser.parse_args()

if __name__ == "__main__":

    # Parsing CLI
    args = cli()
    print(args)
