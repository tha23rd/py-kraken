import argparse

from kraken_aria2 import Kraken

def load_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in-file', dest='infile', default=None, help='path to file containing links to be processed')
    return parser.parse_args()

def load_from_file(fname):
    """
    Load the links from the given file. Each line is considered as one line.
    """
    with open(fname, 'r') as f:
        urls = []
        for line in f:
            # TODO: Add more cleaning and validation to the links
            k = Kraken()
            k.download_file(line.replace('\r', '').replace('\n', ''))
            
    
if __name__ == "__main__":
    args = load_args()
    if args.infile is not None:
        print("Start downloading links......")
        urls = load_from_file(args.infile)
        print("All links downloaded.")
        exit(1)
    else:
        print('Must use input file.')
        exit(1)
    

