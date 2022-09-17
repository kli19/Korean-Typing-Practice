#-----------------------------------------------------------------------
# app.py
# Author: Karen Li
#-----------------------------------------------------------------------

import argparse
from os import name
from sys import argv, stderr, exit
from app import app

#-----------------------------------------------------------------------

def get_args():
    parser = argparse.ArgumentParser(
    description="Korean Typing Practice",
    allow_abbrev=False)
    parser.add_argument("port",
    help="the port at which the server should listen", type=int)
    parser.parse_args()

#-----------------------------------------------------------------------

def main():
    get_args()

    port = int(argv[1])

    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
